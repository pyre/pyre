# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2022 all rights reserved
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

    def __init__(self, uri, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the uri and a string version of it
        self.uri = uri
        self.rep = str(uri)
        # all done
        return


class DirectoryListingError(GenericError):
    """
    Exception raised when something goes wrong with listing the contents of a local directory
    """

    # public data
    description = "error while accessing '{0.uri}': {0.error}"

    # meta-methods
    def __init__(self, error, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.error = error
        # all done
        return


class MountPointError(GenericError):
    """
    Exception generated when the root of a filesystem is invalid
    """

    # public data
    description = "error while mounting '{0.uri}': {0.error}"

    # meta-methods
    def __init__(self, error, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.error = error
        # all done
        return


class FilesystemError(GenericError):
    """
    Base class for all filesystem errors

    Can be used as a catchall when detecting filesystem related exceptions
    """

    def __init__(self, filesystem, node, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.filesystem = filesystem
        self.node = node
        # all done
        return


class NotFoundError(FilesystemError):
    """
    Exception raised when attempting to find a node and the supplied URI does not exist
    """

    # public data
    description = "while looking for {0.rep!r}: {0.fragment!r} not found"

    # meta-methods
    def __init__(self, fragment, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.fragment = fragment
        # all done
        return


class SourceNotFoundError(FilesystemError):
    """
    Exception raised when attempting to find a node and the supplied URI does not exist
    """

    # public data
    description = "while looking for {0.rep!r}: file not found"


class FolderError(FilesystemError):
    """
    Exception raised when a request is made for the contents of a node that is not a folder
    """

    # public data
    description = "while looking for {0.rep!r}: {0.fragment!r} is not a folder"

    # meta-methods
    def __init__(self, fragment, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.fragment = fragment
        # all done
        return


class IsFolderError(FilesystemError):
    """
    Exception raised when a request is made to open a folder
    """

    # public data
    description = "while opening {0.rep!r}: can't open; it is a folder"


class FolderInsertionError(FilesystemError):
    """
    Exception raised when attempting to insert a node in a filsystem and the target node is not
    a folder
    """

    # public data
    description = "error while inserting {0.rep!r}: {0.target!r} is not a folder"

    # meta-methods
    def __init__(self, target, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.target = target
        # all done
        return


class NotRootError(FilesystemError):
    """
    Exception raised when attempting to insert a node with an absolute uri at a location other
    than the root of the filesystem a folder
    """

    # public data
    description = "cannot insert absolute path {0.rep!r} in node {0.target!r}"


class URISpecificationError(GenericError):
    """
    Exception raised when the supplied uri cannot be decoded
    """

    # public data
    description = "{0.rep!r}: {0.reason}"

    # meta-methods
    def __init__(self, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.reason = reason
        # all done
        return


# end of file
