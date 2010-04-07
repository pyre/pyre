# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import time
import zipfile
import weakref
from .Filesystem import Filesystem


class ZipFilesystem(Filesystem):
    """
    Encapsulation of a filesystem that lives inside a zip file

    This capability enable application deployment in zip form
    """


    # interface
    def open(self, node, **kwds):
        """
        Open the file
        """
        # get the info record associated with the node
        info = self.vnodes[node]
        # and call the zipfile open method
        # note that it accepts ZipInfo instances, as well as archive data members
        return self.zipfile.open(info, **kwds)


    def sync(self):
        """
        Populate the filesystem with the contents of the zipfile
        """
        # create a timestamp
        timestamp = time.gmtime()
        # get the archive contents
        for name, info in zip(self.zipfile.namelist(), self.zipfile.infolist()):
            # recognize the type of entry
            # directories end with a slash, everything else is a file
            if name[-1] == '/':
                node = self.newFolder()
            else:
                node = self.newNode()
            # insert the node
            self._insert(node=node, path=name)
            # and attach it to my vnode table
            self.attach(node, info)

        return self

    
    # implementation details
    def attach(self, node, info):
        """
        Added the given {node} and associated information {info} to my vnode table

        This is a low level routine and should not be used directly.
        """
        # add the node to my vnode table
        self.vnodes[node] = info
        # and return it to the caller
        return node


    # meta methods
    def __init__(self, info, vnodes=None, **kwds):
        super().__init__(**kwds)

        # a reference to the zip file i will be serving
        self.zipfile = zipfile.ZipFile(info.uri)

        # storage for information about my nodes
        self.vnodes = vnodes or weakref.WeakKeyDictionary()

        # insert myself to the vnode table
        self.attach(node=self, info=info)

        return


    def __del__(self):
        self.zipfile.close()
        return


# end of file 
