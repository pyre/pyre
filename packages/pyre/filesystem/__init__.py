# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

"""
Support and implementation for a variety of filesystem objects

Explain typical creation/use workflow

Explain virtual, local, remote filesystems

Explain logical structure vs. physical resources

Explain explorers
"""

import os
import re

# NYI:
# it looks like the filesystem creation logic is complicated enough that there should be
# a filesystem factory object, perhaps a singleton, so that there is a chance to simplify

# NYI:
# teach explorers to ask the filesystem for the file type marker

# top level factory
def newFilesystem(uri=None, **kwds):
    """
    Create a new filesystem object whose type is appropriate for the given uri

    parameters: 
        {uri}: a specification of the root of the filesystem that may include information about
        the type of filesystem required
    """

    # a missing uri implies a virtual filesystem
    if uri is None:
        return newVirtualFilesystem(**kwds)
    # attempt to parse {uri}
    spec = uriRecognizer.match(uri)
    if spec is None:
        raise MountPointError(path=uri, error="unrecognizable URI specification")
    # extract the method
    method = spec.group("method")
    if method is None:
        method = "file"
    else:
        method = method.strip().lower()
    # lookup the method handler and invoke it
    try:
        return registry[method](root=spec.group("address"), **kwds)
    except KeyError:
        pass
    # otherwise
    raise MountPointError(path=uri, description="unrecognizable URI specification")


# factories for filesystems
def newLocalFilesystem(root, walker=None, recognizer=None, **kwds):
    """
    Factory for a local filesystem, i.e. one that encapsulates the contents of a filesystem
    that is mounted on the machine that hosts the caller's process
    
    parameters:
        {root}: the directory to use as the root of the new filesystem
        {walker}: the mechanism that lists the contents of directories
        {recognizer}: the mechanism that identifies the types of files
    """
    # NYI:
    # check that we have read/execute permissions so we can get the directory listing
    # let it be for now, so i can figure out what exceptions get generated

    # build a walker and a recognizer, if necessary
    walker = walker or newDirectoryWalker()
    recognizer = recognizer or newStatRecognizer()

    # ensure that {root} is an absolute path so that we can protect the filesystem
    # representation in case the application manipulates the current working directory of the
    # process
    root = os.path.abspath(root)
    # check that it is an existing path
    try:
        node = recognizer.recognize(root)
    except OSError:
        raise MountPointError(path=root, error="mount point not found")
    # verify it is a directory; i really don't like code like this...
    from .File import File
    from .Directory import Directory
    if isinstance(node, Directory):
        # build the filesystem
        from .LocalFilesystem import LocalFilesystem
        fs = LocalFilesystem(info=node, walker=walker, recognizer=recognizer, **kwds)
        # populate it
        fs.sync()
        # and return it to the caller
        return fs
    elif isinstance(node, File):
        import zipfile
        if zipfile.is_zipfile(root):
            # build the file system
            from .ZipFilesystem import ZipFilesystem
            fs = ZipFilesystem(info=node)
            # populate it
            fs.sync()
            # and return it
            return fs
    # otherwise
    raise MountPointError(path=root, error="invalid mount point")


def newVirtualFilesystem(root='/', **kwds):
    """
    Factory for a virtual filesystem, i.e. one whose contents are not necessarily physical
    resources

    Virtual filesystems are useful as abstract namespaces that decouple the physical location
    of resources from the identifiers that application use to refer to them
    """
    from .Filesystem import Filesystem
    return Filesystem(**kwds)


def newZipFilesystem(root, recognizer=None, **kwds):
    """
    Factory for a filesystem object that serves the contents of a zipfile

    parameters:
        {root}: the path to the zipfile
    """

    # ensure that root is absolute, just in case the app changes the current working directory
    root = os.path.abspath(root)
    # check that it is a zipfile
    import zipfile
    if not zipfile.is_zipfile(root):
        raise MountPointError(path=root, error="mount point is not a zipfile")
    # get the recognizer to build an info object for the archive
    recognizer = recognizer or newStatRecognizer()
    info = recognizer.recognize(root)

    # build the file system
    from .ZipFilesystem import ZipFilesystem
    fs = ZipFilesystem(info=info)
    # populate it
    fs.sync()
    # and return it
    return fs


# other factories
def newFinder(**kwds):
    """
    Create a filesystem explorer that returns the contents of a filesystem
    """
    from .Finder import Finder
    return Finder(**kwds)


def newSimpleExplorer(**kwds):
    """
    Create a filesystem explorer that creates a simple report of the filesystem contents
    """
    from .SimpleExplorer import SimpleExplorer
    return SimpleExplorer(**kwds)


def newTreeExplorer(**kwds):
    """
    Create a filesystem explorer that creates a tree-like report of the filesystem contents
    """
    from .TreeExplorer import TreeExplorer
    return TreeExplorer(**kwds)


def newDirectoryWalker(**kwds):
    """
    Mechanism for listing the contents of local directories
    """
    from .DirectoryWalker import DirectoryWalker
    return DirectoryWalker(**kwds)


def newStatRecognizer(**kwds):
    """
    Mechanism for extracting information about local files
    """
    from .StatRecognizer import StatRecognizer
    return StatRecognizer(**kwds)


# package constants
PATH_SEPARATOR = '/'


# other implementation details
uriRecognizer = re.compile(r"((?P<method>[^:]+)://)?(?P<address>.*)")

registry = {
    None: newLocalFilesystem,
    "vfs": newVirtualFilesystem,
    "file": newLocalFilesystem,
    "zip": newZipFilesystem,
    }


# exceptions throwm bu the factories
from .exceptions import MountPointError


# debugging support: 
#     import the package and set to something else, e.g. pyre.patterns.ExtentAware
#     to change the runtime behavior of these objects
_metaclass_Node = type
_metaclass_Filesystem = type


def debug():
    """
    Attach ExtentAware as the metaclass of Node and Filesystem so we can verify that all
    instances of these classes are properly garbage collected
    """
    from ..patterns.ExtentAware import ExtentAware
    global _metaclass_Node, _metaclass_Filesystem
    _metaclass_Node = ExtentAware
    _metaclass_Filesystem = ExtentAware

    return
    

# end of file 
