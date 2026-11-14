"""Refuse link/junction/reparse-point ancestry and ".." aliases for all local IO.

Python 3.11-compatible: uses lstat for each existing path component. Supports
Windows FILE_ATTRIBUTE_REPARSE_POINT without assuming pathlib.is_junction().
This is a local guard, not a substitute for secure directory handles and ACLs.
"""
from pathlib import Path
import stat

REPARSE=getattr(stat,"FILE_ATTRIBUTE_REPARSE_POINT",0x400)

def assert_no_links(value, *, allow_missing_leaf=False):
    path=Path(value).absolute()
    if ".." in path.parts:
        raise ValueError("Parent-directory alias forbidden")
    nodes=(path,*path.parents)
    for index,node in enumerate(nodes):
        try:
            information=node.lstat()
        except FileNotFoundError as error:
            if index==0 and allow_missing_leaf:
                continue
            raise ValueError("Missing path component") from error
        if stat.S_ISLNK(information.st_mode) or (
                getattr(information,"st_file_attributes",0)&REPARSE):
            raise ValueError("Symbolic link, junction or reparse point forbidden")
    return path

def _open_source_readonly(path, flags):
    """Open a source so other processes cannot write/delete it during the read."""
    import os
    if os.name!="nt":
        return os.open(path,flags)

    import ctypes
    import msvcrt
    from ctypes import wintypes

    kernel32=ctypes.WinDLL("kernel32",use_last_error=True)
    create_file=kernel32.CreateFileW
    create_file.argtypes=(
        wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,
        wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE
    )
    create_file.restype=wintypes.HANDLE
    close_handle=kernel32.CloseHandle
    close_handle.argtypes=(wintypes.HANDLE,)
    close_handle.restype=wintypes.BOOL

    # FILE_SHARE_READ deliberately excludes FILE_SHARE_WRITE and FILE_SHARE_DELETE.
    handle=create_file(
        str(path),
        0x80000000,  # GENERIC_READ
        0x00000001,  # FILE_SHARE_READ
        None,
        3,           # OPEN_EXISTING
        0x00000080,  # FILE_ATTRIBUTE_NORMAL
        None,
    )
    handle_value=handle if isinstance(handle,int) else getattr(handle,"value",None)
    if handle_value is None or handle_value==ctypes.c_void_p(-1).value:
        error_code=ctypes.get_last_error()
        if error_code==32:  # ERROR_SHARING_VIOLATION
            raise PermissionError(
                13,"Source has incompatible concurrent write access",
                str(path),error_code
            )
        raise ctypes.WinError(error_code)

    try:
        return msvcrt.open_osfhandle(
            handle_value,os.O_RDONLY|os.O_BINARY
        )
    except BaseException:
        close_handle(wintypes.HANDLE(handle_value))
        raise

def read_bounded_source(path, *, max_bytes=8_000_000):
    """Read a bounded regular source via one handle and verify file identity.

    Uses O_NOFOLLOW where supported and compares path/handle metadata.
    On Windows, the read handle also denies concurrent write/delete sharing for
    the file's lifetime. Directory ancestry remains subject to TOCTOU limits.
    """
    import os
    path=assert_no_links(path)
    before=path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size>max_bytes:
        raise ValueError("Source must be a bounded regular file")
    flags=os.O_RDONLY|getattr(os,"O_BINARY",0)|getattr(os,"O_NOFOLLOW",0)
    descriptor=_open_source_readonly(path,flags)
    try:
        start=os.fstat(descriptor)
        if not stat.S_ISREG(start.st_mode) or start.st_size>max_bytes:
            raise ValueError("Source changed type or exceeded limit")
        if (start.st_dev,start.st_ino)!=(before.st_dev,before.st_ino):
            raise ValueError("Source path was replaced before reading")
        chunks=[]
        total=0
        while total<=max_bytes:
            data=os.read(descriptor,min(65536,max_bytes+1-total))
            if not data:
                break
            total+=len(data)
            if total>max_bytes:
                raise ValueError("Source exceeds bounded read limit")
            chunks.append(data)
        after=os.fstat(descriptor)
        end=assert_no_links(path).lstat()
    finally:
        os.close(descriptor)
    first=(start.st_dev,start.st_ino,start.st_size,start.st_mtime_ns,start.st_ctime_ns)
    second=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    final=(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns,end.st_ctime_ns)
    if first!=second or first!=final or total!=start.st_size:
        raise ValueError("Source changed during bounded file-handle read")
    return b"".join(chunks)
