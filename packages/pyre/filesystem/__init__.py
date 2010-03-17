# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


# errors
class FilesystemError(Exception):
    """
    Base class for all filesystem errors

    Can be used as a catchall when detecting filesystem related exceptions
    """

    def __init__(self, fs, node, message, **kwds):
        super().__init__(**kwds)
        self.fs = fs
        self.node = node
        self.message = message
        return

    def __str__(self):
        return self.message


class FolderError(FilesystemError):

    def __init__(self, fs, folder, path, target, **kwds):
        msg = "error while inserting {0!r}: {1!r} is not a folder".format(path, target)
        super().__init__(fs, folder, msg, **kwds)
        self.path = path
        self.target = target
        return


# package constants
PATH_SEPARATOR = '/'


# debugging support
_metaclass_Node = type
_metaclass_Filesystem = type

# end of file 
