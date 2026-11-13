"""Refuse link/junction/reparse-point ancestry and ".." aliases for all local IO.

Python 3.11-compatible: uses lstat for each existing path component. Supports
Windows FILE_ATTRIBUTE_REPARSE_POINT without assuming pathlib.is_junction().
This is a local guard, not a substitute for exclusive file handles and owner ACLs.
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

def read_bounded_source(path, *, max_bytes=8_000_000):
    """Read a bounded regular source via one handle and verify file identity.

    Uses O_NOFOLLOW on systems supporting it and lstat/fstat before/after.
    This narrows pathname swap races but does NOT make a customer-controlled
    Windows directory an atomic/signed snapshot or defend against all TOCTOU.
    """
    import os
    path=assert_no_links(path)
    before=path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size>max_bytes:
        raise ValueError("Source must be a bounded regular file")
    flags=os.O_RDONLY|getattr(os,"O_BINARY",0)|getattr(os,"O_NOFOLLOW",0)
    descriptor=os.open(path,flags)
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
    finally:
        os.close(descriptor)
    end=assert_no_links(path).lstat()
    first=(start.st_dev,start.st_ino,start.st_size,start.st_mtime_ns,start.st_ctime_ns)
    second=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    final=(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns,end.st_ctime_ns)
    if first!=second or first!=final or total!=start.st_size:
        raise ValueError("Source changed during bounded file-handle read")
    return b"".join(chunks)
