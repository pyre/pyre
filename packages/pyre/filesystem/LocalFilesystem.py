# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import time
from .Filesystem import Filesystem


class LocalFilesystem(Filesystem):
    """
    Encapsulation of a filesystem local to the machine on which the application is runing

    LocalFilsystem uses listdir, (l)stat and other C library routines appropriate for locally
    mounted filesystems to discover and serve its contents
    """


    # public data
    walker = None # the directory listing mechanism
    recognizer = None # the file type recognizer

    @property
    def mountpoint(self):
        """
        The location of my root
        """
        return self.vnodes[self].uri


    # interface
    def sync(self, walker=None, recognizer=None):
        """
        Traverse my directory structure and refresh my contents so that they match the
        underlying filesystem
        """
        # create a timestamp
        timestamp = time.gmtime()
        # use the explicitly supplied traversal support, if available
        walker = walker or self.walker
        recognizer = recognizer or self.recognizer
        # initialize the traversal at my root
        todo = [ self ]
        # and start walking and recognizing
        for folder in todo:
            # compute the actual location of this directory
            location = self.vnodes[folder].uri
            # walk through the contents
            for entry in walker.walk(location):
                # build the absolute path of the entry
                address = os.path.join(location, entry)
                # recognize the file
                factory, metadata = recognizer.recognize(address)
            

        return


    # implementation details
    def attach(self, node, info):
        """
        Added the given {node} and associated information {info} to my vnode table

        This is a low level routine and should not be used directly. It is meant to be
        overriden by descendants of LocalFilesystem to support alternative vnode storage
        behavior
        """
        # add the node to my vnode table
        self.vnodes[node] = info
        # and return it to the caller
        return node


    # meta methods
    def __init__(self, info, recognizer, walker, vnodes=None, **kwds):
        super().__init__(**kwds)

        # register the discovery mechanisms
        self.walker = walker
        self.recognizer = recognizer

        # storage for information about my nodes
        # if descendants provide a custom container, use it; otherwise use a dictionary
        # descendants must remember to override self.attach to match the custom container
        self.vnodes = vnodes or dict()

        # insert myself to the vnode table
        self.attach(node=self, info=info)

        return


# end of file 
