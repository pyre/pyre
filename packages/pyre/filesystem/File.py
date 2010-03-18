# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import stat


class File(object):
    """
    The base class for local filesystem entries
    """

    # public data
    uri = None # the actual address of the file
    owner = None # the owner of the node
    uid = gid = None # the user and group ids of the current owner
    size = None # the actual size of the file
    permissions = None # NYI
    syncTime = None # the last time this vnode was compared against reality

    # time stamps as reported by the underlying filesystem
    accessTime = None # the time of last access
    creationTime = None # the creation time
    modificationTime = None # the time this file was last modified


    # interface
    def isDirectory(self):
        """
        Quick check of whether this node represents a folder or not
        """
        return False


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


    # meta methods
    def __init__(self, uri, info=None, **kwds):
        super().__init__(**kwds)

        # attach my uri
        self.uri = uri
        # extract the file metadata from info
        info and self.decorate(info)

        return


    # constant
    marker = 'f'

    
# end of file 
