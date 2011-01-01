# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

"""
Definitions for all the exceptions raised by this package
"""

from ..framework.exceptions import FrameworkError


class GenericError(FrameworkError):
    """
    Base class for all errors in this package

    Can be used as a catchall when detecting errors generated by this package
    """


class DirectoryListingError(GenericError):
    """
    Exception raised when something goes wrong with listing the contents of a local directory
    """

    def __init__(self, path, error, **kwds):
        msg = "error while accessing {0!r}: {1}".format(path, error)
        super().__init__(description=msg, **kwds)
        self.path = path
        return


class MountPointError(GenericError):
    """
    Exception generated when the root of a filesystem is invalid
    """

    def __init__(self, path, error):
        msg = "error while mounting {0!r}: {1}".format(path, error)
        super().__init__(description=msg)
        self.path = path
        return


class FilesystemError(GenericError):
    """
    Base class for all filesystem errors

    Can be used as a catchall when detecting filesystem related exceptions
    """

    def __init__(self, filesystem, node, **kwds):
        super().__init__(**kwds)
        self.filesystem = filesystem
        self.node = node
        return


class NotFoundError(FilesystemError):
    """
    Exception raised when attempting to find a node and the supplied URI does not exist
    """

    def __init__(self, path, fragment, **kwds):
        msg = "while looking for {0!r}: {1!r} not found".format(path, fragment)
        super().__init__(description=msg, **kwds)
        self.path = path
        self.fragment = fragment
        return


class FolderInsertionError(FilesystemError):
    """
    Exception raised when attempting to insert a node in a filsystem and the target node is not
    a folder
    """

    def __init__(self, path, target, **kwds):
        msg = "error while inserting {0!r}: {1!r} is not a folder".format(path, target)
        super().__init__(description=msg, **kwds)
        self.path = path
        self.target = target
        return


class URISpecificationError(GenericError):
    """
    Exception raised when the supplied uri cannot be decoded
    """

    def __init__(self, uri, **kwds):
        super().__init__(**kwds)
        self.uri = uri
        return


# end of file 
