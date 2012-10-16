# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import stat
# superclass
from .metadata import Info


# class declaration
class File(Info):
    """
    The base class for local filesystem entries
    """

    # constants
    marker = 'f'
    isDirectory = False


    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a file
        """
        return explorer.onFile(self, **kwds)


    def decorate(self, info):
        """
        Extract useful file metadata from a stat-compatible data structure
        """
        self.uid = info.st_uid
        self.gid = info.st_gid
        self.size = info.st_size
        self.permissions = stat.S_IMODE(info.st_mode)

        self.accessTime = info.st_atime
        self.creationTime = info.st_ctime
        self.modificationTime = info.st_mtime

        return


    # debugging support
    def dump(self):
        """
        Print out the known information about this file
        """
        import time
        print("node {}".format(self))
        print("  uri:", self.uri)
        print("  uid:", self.uid)
        print("  gid:", self.gid)
        print("  size:", self.size)
        print("  permissions: {:o}".format(self.permissions))
        print("  access time:", time.asctime(time.localtime(self.accessTime)))
        print("  creation time:", time.asctime(time.localtime(self.creationTime)))
        print("  modification time:", time.asctime(time.localtime(self.modificationTime)))


    # meta methods
    def __init__(self, info=None, **kwds):
        super().__init__(**kwds)
        # extract the file metadata from info
        info and self.decorate(info)
        # all done
        return


    # implementation details
    __slots__ = (
        'uid', 'gid', # the user and group ids of the current owner
        'size', # the actual size of the file
        'permissions', # NYI
        #
        'syncTime', # the last time this vnode was compared against reality
        # time stamps as reported by the underlying filesystem
        'accessTime', # the time of last access
        'creationTime', # the creation time
        'modificationTime', # the time this file was last modified
        )

    
# end of file 
