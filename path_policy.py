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
