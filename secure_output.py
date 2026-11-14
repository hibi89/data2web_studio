"""Handle-relative create-only output to avoid parent-path redirection races."""
from __future__ import annotations

import ctypes
import errno
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


class OutputDirectory:
    """A pinned output directory; children are created relative to its handle."""

    def __init__(self, path, handle):
        self.path = Path(path).absolute()
        self._handle = handle
        self._closed = False

    @classmethod
    def open(cls, value):
        path = Path(value).absolute()
        assert_no_links(path)
        before = path.lstat()
        if not stat.S_ISDIR(before.st_mode) or _is_reparse(before):
            raise ValueError("Output parent must be a real directory")
        if os.name == "nt":
            handle = _windows_open_directory(path, before)
        else:
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
            try:
                handle = os.open(path, flags)
            except OSError as error:
                raise ValueError("Output parent changed during validation") from error
            try:
                opened = os.fstat(handle)
                assert_no_links(path)
                after = path.lstat()
                if (not stat.S_ISDIR(opened.st_mode) or
                        _identity(opened) != _identity(before) or
                        _identity(opened) != _identity(after)):
                    raise ValueError("Output parent changed during validation")
            except BaseException:
                os.close(handle)
                raise
        return cls(path, handle)

    def create_file(self, name, mode=0o600):
        self._ensure_open()
        _validate_leaf(name)
        if os.name == "nt":
            handle = _windows_create_relative(
                self._handle, name, directory=False
            )
            import msvcrt
            descriptor = msvcrt.open_osfhandle(
                handle, os.O_WRONLY | getattr(os, "O_BINARY", 0)
            )
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
            handle = _windows_create_relative(
                self._handle, name, directory=True
            )
            info = _windows_handle_info(handle)
            if not info.dwFileAttributes & 0x10 or info.dwFileAttributes & REPARSE:
                _windows_close(handle)
                raise ValueError("Created output directory failed identity checks")
            return OutputDirectory(child_path, handle)
        os.mkdir(name, mode, dir_fd=self._handle)
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        try:
            child = os.open(name, flags, dir_fd=self._handle)
            opened = os.fstat(child)
            named = os.stat(name, dir_fd=self._handle, follow_symlinks=False)
            if (not stat.S_ISDIR(opened.st_mode) or
                    _identity(opened) != _identity(named)):
                os.close(child)
                raise ValueError("Created output directory failed identity checks")
            return OutputDirectory(child_path, child)
        except BaseException:
            raise

    def _ensure_open(self):
        if self._closed:
            raise ValueError("Output directory handle is closed")

    def close(self):
        if self._closed:
            return
        self._closed = True
        if os.name == "nt":
            _windows_close(self._handle)
        else:
            os.close(self._handle)

    def __enter__(self):
        self._ensure_open()
        return self

    def __exit__(self, *_exc):
        self.close()


def open_output_directory(value):
    return OutputDirectory.open(value)


def create_output_directory(value, mode=0o700):
    """Create and return a pinned, new directory under a pinned parent."""
    path = Path(value).absolute()
    assert_no_links(path, allow_missing_leaf=True)
    if path.exists() or path.is_symlink():
        raise FileExistsError("Output directory must be new")
    with open_output_directory(path.parent) as parent:
        child = parent.create_directory(path.name, mode)
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
        info = _windows_handle_info(directory._handle)
        return info.dwVolumeSerialNumber, (
            (info.nFileIndexHigh << 32) | info.nFileIndexLow
        )
    info = os.fstat(directory._handle)
    return _identity(info)


def create_output_file(value, *, directory=None, mode=0o600):
    """Create a new file relative to a verified, held directory handle."""
    path = Path(value).absolute()
    _validate_leaf(path.name)
    if directory is not None:
        if not isinstance(directory, OutputDirectory) or path.parent != directory.path:
            raise ValueError("Output directory handle does not match target parent")
        return directory.create_file(path.name, mode)
    with open_output_directory(path.parent) as parent:
        return parent.create_file(path.name, mode)


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
    handle = kernel32.CreateFileW(
        str(path),
        0x00000001 | 0x00000080,  # FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES
        0x00000001 | 0x00000002 | 0x00000004,  # share read/write/delete
        None, 3, 0x02000000 | 0x00200000, None,  # backup + open reparse point
    )
    value = handle if isinstance(handle, int) else getattr(handle, "value", None)
    invalid = ctypes.c_void_p(-1).value
    if value is None or value == invalid:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        info = _windows_handle_info(handle)
        assert_no_links(path)
        after = path.lstat()
        identity = _windows_identity(info)
        if (not info.dwFileAttributes & 0x10 or
                info.dwFileAttributes & REPARSE or
                identity != _identity(before) or identity != _identity(after)):
            raise ValueError("Output parent changed during validation")
        return handle
    except BaseException:
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

    buffer = ctypes.create_unicode_buffer(name)
    object_name = UNICODE_STRING(
        len(name.encode("utf-16-le")), len(name.encode("utf-16-le")) + 2,
        ctypes.cast(buffer, wintypes.LPWSTR),
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
    desired_access = 0x40000000 | 0x00100000  # GENERIC_WRITE | SYNCHRONIZE
    file_attributes = 0x10 if directory else 0x80
    create_options = (0x00000001 if directory else 0x00000040) | 0x00000020
    status = create_file(
        ctypes.byref(output_handle), desired_access,
        ctypes.byref(attributes), ctypes.byref(status_block),
        None, file_attributes, 0x00000001 | 0x00000002 | 0x00000004,
        2, create_options, None, 0,  # FILE_CREATE
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
