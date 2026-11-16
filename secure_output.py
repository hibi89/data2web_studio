"""Handle-relative, create-only output under trusted directory ancestry."""
from __future__ import annotations

import ctypes
import os
import stat
from pathlib import Path

from path_policy import REPARSE, assert_no_links


def _identity(info):
    return info.st_dev, info.st_ino


def _is_reparse(info):
    return bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def _validate_leaf(name):
    if (not isinstance(name, str) or not name or name in (".", "..") or
            Path(name).name != name or "/" in name or "\\" in name or
            any(ord(char) < 32 or ord(char) == 127 for char in name)):
        raise ValueError("Output name must be one local basename")
    if len(name) > 255:
        raise ValueError("Output name is too long")
    if os.name == "nt":
        if any(char in '<>:"|?*' for char in name) or name.endswith((" ", ".")):
            raise ValueError("Output name contains an unsafe Windows character")
        device = name.split(".", 1)[0].upper()
        if device in {"CON", "PRN", "AUX", "NUL"} or (
                len(device) == 4 and device[:3] in {"COM", "LPT"} and
                device[3] in "123456789"):
            raise ValueError("Output name is a reserved Windows device")


def _assert_trusted_posix_ancestry(path):
    """Require owner-controlled ancestry; allow sticky shared temp roots."""
    uid = os.geteuid()
    nodes = (path, *path.parents)
    for index, node in enumerate(nodes):
        info = node.lstat()
        if (not stat.S_ISDIR(info.st_mode) or _is_reparse(info) or
                info.st_uid not in (0, uid)):
            raise ValueError("Output ancestry is not owned by a trusted account")
        mode = stat.S_IMODE(info.st_mode)
        if mode & (stat.S_IWGRP | stat.S_IWOTH):
            if not mode & stat.S_ISVTX:
                raise ValueError("Output ancestry is writable by other users")
            if index:
                child = nodes[index - 1].lstat()
                if child.st_uid not in (0, uid):
                    raise ValueError("Shared sticky ancestry has an untrusted child")
    # This local permission check treats other user IDs as untrusted. A process
    # running as the same UID remains trusted; POSIX has no directory rename lock.


class OutputDirectory:
    """A pinned directory handle; child creates stay relative to this directory."""

    def __init__(self, path, handle, handles=None):
        self.path = Path(path).absolute()
        self._handles = list(handles) if handles is not None else [handle]
        self._handle = self._handles[-1]
        self._closed = False

    @classmethod
    def open(cls, value, expected_identity=None):
        path = Path(value).absolute()
        assert_no_links(path)
        before = path.lstat()
        if not stat.S_ISDIR(before.st_mode) or _is_reparse(before):
            raise ValueError("Output parent must be a real directory")
        if expected_identity is not None and _identity(before) != expected_identity:
            raise ValueError("Output parent changed during validation")
        if os.name == "nt":
            handles = _windows_open_directory(path, before)
            return cls(path, handles[-1], handles=handles)
        _assert_trusted_posix_ancestry(path)
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        try:
            handle = os.open(path, flags)
        except OSError as error:
            raise ValueError("Output parent changed during validation") from error
        try:
            opened = os.fstat(handle)
            assert_no_links(path)
            _assert_trusted_posix_ancestry(path)
            after = path.lstat()
            if (not stat.S_ISDIR(opened.st_mode) or
                    _identity(opened) != _identity(before) or
                    _identity(opened) != _identity(after) or
                    (expected_identity is not None and
                     _identity(opened) != expected_identity)):
                raise ValueError("Output parent changed during validation")
        except BaseException:
            os.close(handle)
            raise
        return cls(path, handle)

    def create_file(self, name, mode=0o600):
        self._ensure_open()
        _validate_leaf(name)
        if os.name == "nt":
            handle = _windows_create_relative(self._handle, name, directory=False)
            import msvcrt
            try:
                descriptor = msvcrt.open_osfhandle(
                    handle, os.O_WRONLY | getattr(os, "O_BINARY", 0)
                )
            except BaseException:
                _windows_close(handle)
                raise
        else:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
            descriptor = os.open(name, flags, mode, dir_fd=self._handle)
        return os.fdopen(descriptor, "wb")

    def create_directory(self, name, mode=0o700):
        self._ensure_open()
        _validate_leaf(name)
        child_path = self.path / name
        if os.name == "nt":
            handle = _windows_create_relative(self._handle, name, directory=True)
            try:
                info = _windows_handle_info(handle)
                if not info.dwFileAttributes & 0x10 or info.dwFileAttributes & REPARSE:
                    raise ValueError("Created output directory failed identity checks")
                return OutputDirectory(
                    child_path, handle, handles=self._handles + [handle]
                )
            except BaseException:
                _windows_close(handle)
                raise
        os.mkdir(name, mode, dir_fd=self._handle)
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        child = os.open(name, flags, dir_fd=self._handle)
        try:
            opened = os.fstat(child)
            named = os.stat(name, dir_fd=self._handle, follow_symlinks=False)
            if (not stat.S_ISDIR(opened.st_mode) or
                    _identity(opened) != _identity(named)):
                raise ValueError("Created output directory failed identity checks")
            return OutputDirectory(child_path, child)
        except BaseException:
            os.close(child)
            raise

    def _ensure_open(self):
        if self._closed:
            raise ValueError("Output directory handle is closed")

    def close(self):
        if self._closed:
            return
        self._closed = True
        if os.name == "nt":
            for handle in reversed(self._handles):
                _windows_close(handle)
        else:
            os.close(self._handle)

    def __enter__(self):
        self._ensure_open()
        return self

    def __exit__(self, *_exc):
        self.close()


class _ManagedOutputFile:
    """Keep a privately opened directory pinned until the output stream closes."""

    def __init__(self, stream, directory=None):
        self._stream = stream
        self._directory = directory
        self._closed = False

    def __enter__(self):
        return self._stream

    def __exit__(self, *_exc):
        self.close()

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            self._stream.close()
        finally:
            if self._directory is not None:
                self._directory.close()


def open_output_directory(value, *, expected_identity=None):
    return OutputDirectory.open(value, expected_identity=expected_identity)


def create_output_directory(value, mode=0o700):
    """Create and return a pinned, new directory under a pinned parent."""
    path = Path(value).absolute()
    assert_no_links(path, allow_missing_leaf=True)
    if path.exists() or path.is_symlink():
        raise FileExistsError("Output directory must be new")
    parent_info = path.parent.lstat()
    parent = open_output_directory(
        path.parent, expected_identity=_identity(parent_info)
    )
    try:
        child = parent.create_directory(path.name, mode)
        if os.name == "nt":
            # The child handle also retains the full no-delete ancestor chain.
            parent._closed = True
        else:
            parent.close()
    except BaseException:
        parent.close()
        raise
    try:
        assert_no_links(path)
        named = path.lstat()
        if _identity(named) != _directory_identity(child):
            raise ValueError("Created output directory changed during validation")
    except BaseException:
        child.close()
        raise
    return child


def _directory_identity(directory):
    if os.name == "nt":
        return _windows_identity(_windows_handle_info(directory._handle))
    return _identity(os.fstat(directory._handle))


def create_output_file(value, *, directory=None, mode=0o600):
    """Create a new file relative to a verified, held directory handle."""
    path = Path(value).absolute()
    _validate_leaf(path.name)
    if directory is not None:
        if not isinstance(directory, OutputDirectory) or path.parent != directory.path:
            raise ValueError("Output directory handle does not match target parent")
        return _ManagedOutputFile(directory.create_file(path.name, mode))
    parent = open_output_directory(path.parent)
    try:
        stream = parent.create_file(path.name, mode)
    except BaseException:
        parent.close()
        raise
    return _ManagedOutputFile(stream, parent)


def _windows_api():
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    )
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD),
                    ("dwHighDateTime", wintypes.DWORD)]

    class BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", wintypes.DWORD),
            ("ftCreationTime", FILETIME),
            ("ftLastAccessTime", FILETIME),
            ("ftLastWriteTime", FILETIME),
            ("dwVolumeSerialNumber", wintypes.DWORD),
            ("nFileSizeHigh", wintypes.DWORD),
            ("nFileSizeLow", wintypes.DWORD),
            ("nNumberOfLinks", wintypes.DWORD),
            ("nFileIndexHigh", wintypes.DWORD),
            ("nFileIndexLow", wintypes.DWORD),
        ]

    kernel32.GetFileInformationByHandle.argtypes = (
        wintypes.HANDLE, ctypes.POINTER(BY_HANDLE_FILE_INFORMATION),
    )
    kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
    return kernel32, BY_HANDLE_FILE_INFORMATION


def _windows_handle_info(handle):
    kernel32, info_type = _windows_api()
    info = info_type()
    if not kernel32.GetFileInformationByHandle(handle, ctypes.byref(info)):
        raise ctypes.WinError(ctypes.get_last_error())
    return info


def _windows_identity(info):
    return info.dwVolumeSerialNumber, (
        (info.nFileIndexHigh << 32) | info.nFileIndexLow
    )


def _windows_open_directory(path, before):
    kernel32, _ = _windows_api()
    nodes = list(reversed((path, *path.parents)))
    snapshots = []
    for node in nodes:
        info = node.lstat()
        if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
            raise ValueError("Output ancestry changed during validation")
        snapshots.append((node, _identity(info)))
    if snapshots[-1][1] != _identity(before):
        raise ValueError("Output parent changed during validation")

    handles = []
    try:
        for node, expected in snapshots:
            handle = kernel32.CreateFileW(
                str(node),
                0x00000001 | 0x00000080,  # FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES
                0x00000001 | 0x00000002,  # share read/write; deny delete/rename
                None, 3, 0x02000000 | 0x00200000, None,
            )
            value = handle if isinstance(handle, int) else getattr(handle, "value", None)
            invalid = ctypes.c_void_p(-1).value
            if value is None or value == invalid:
                raise ctypes.WinError(ctypes.get_last_error())
            handles.append(handle)
            info = _windows_handle_info(handle)
            identity = _windows_identity(info)
            if (not info.dwFileAttributes & 0x10 or
                    info.dwFileAttributes & REPARSE or identity != expected):
                raise ValueError("Output ancestry changed during validation")
        assert_no_links(path)
        if _identity(path.lstat()) != snapshots[-1][1]:
            raise ValueError("Output parent changed during validation")
        return handles
    except BaseException:
        for handle in reversed(handles):
            _windows_close(handle)
        raise


def _windows_create_relative(root, name, *, directory):
    from ctypes import wintypes

    class UNICODE_STRING(ctypes.Structure):
        _fields_ = [("Length", wintypes.USHORT),
                    ("MaximumLength", wintypes.USHORT),
                    ("Buffer", wintypes.LPWSTR)]

    class OBJECT_ATTRIBUTES(ctypes.Structure):
        _fields_ = [
            ("Length", wintypes.ULONG),
            ("RootDirectory", wintypes.HANDLE),
            ("ObjectName", ctypes.POINTER(UNICODE_STRING)),
            ("Attributes", wintypes.ULONG),
            ("SecurityDescriptor", wintypes.LPVOID),
            ("SecurityQualityOfService", wintypes.LPVOID),
        ]

    class IO_STATUS_BLOCK(ctypes.Structure):
        _fields_ = [("Status", ctypes.c_long), ("Information", ctypes.c_void_p)]

    encoded_length = len(name.encode("utf-16-le"))
    buffer = ctypes.create_unicode_buffer(name)
    object_name = UNICODE_STRING(
        encoded_length, encoded_length + 2, ctypes.cast(buffer, wintypes.LPWSTR)
    )
    attributes = OBJECT_ATTRIBUTES(
        ctypes.sizeof(OBJECT_ATTRIBUTES), root,
        ctypes.pointer(object_name), 0x40, None, None,  # OBJ_CASE_INSENSITIVE
    )
    status_block = IO_STATUS_BLOCK()
    output_handle = wintypes.HANDLE()
    ntdll = ctypes.WinDLL("ntdll")
    create_file = ntdll.NtCreateFile
    create_file.argtypes = (
        ctypes.POINTER(wintypes.HANDLE), wintypes.ULONG,
        ctypes.POINTER(OBJECT_ATTRIBUTES), ctypes.POINTER(IO_STATUS_BLOCK),
        ctypes.c_void_p, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG,
        wintypes.ULONG, ctypes.c_void_p, wintypes.ULONG,
    )
    create_file.restype = ctypes.c_long
    desired_access = 0x40000000 | 0x00000080 | 0x00100000
    file_attributes = 0x10 if directory else 0x80
    create_options = (0x00000001 if directory else 0x00000040) | 0x00000020
    status = create_file(
        ctypes.byref(output_handle), desired_access,
        ctypes.byref(attributes), ctypes.byref(status_block),
        None, file_attributes, 0x00000001 | 0x00000002,
        2, create_options, None, 0,  # FILE_CREATE; no delete sharing
    )
    if status < 0:
        dos_error = ntdll.RtlNtStatusToDosError(status)
        if dos_error in (80, 183):
            raise FileExistsError(dos_error, "Output already exists", name)
        raise ctypes.WinError(dos_error)
    return output_handle.value


def _windows_close(handle):
    kernel32, _ = _windows_api()
    if not kernel32.CloseHandle(handle):
        raise ctypes.WinError(ctypes.get_last_error())
