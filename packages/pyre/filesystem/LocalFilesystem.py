# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import time
import weakref
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
    def open(self, node, **kwds):
        """
        Open the file
        """
        # get the info record associated with the node
        info = self.vnodes[node]
        # extract the actual filename
        uri = info.uri
        # and call the system open
        return open(uri, **kwds)


    def sync(self, walker=None, recognizer=None, root=None, levels=None):
        """
        Traverse my directory structure and refresh my contents so that they match the
        underlying filesystem
        """
        # create a timestamp
        timestamp = time.gmtime()
        # use the explicitly supplied traversal support, if available
        walker = walker or self.walker
        recognizer = recognizer or self.recognizer
        # establish the starting point
        root = root if root is not None else self
        # initialize the traversal at my root
        todo = [ (root, 0) ]
        # and start walking and recognizing
        for folder, level in todo:
            # should we process?
            if levels is not None and level >= levels: continue
            # compute the actual location of this directory
            location = self.vnodes[folder].uri
            # walk through the contents
            for entry in walker.walk(location):
                # build the absolute path of the entry
                address = os.path.join(location, entry)
                # recognize the file and timestap it
                nodeInfo = recognizer.recognize(address)
                nodeInfo.syncTime = timestamp
                # decide what kind of node to build
                if nodeInfo.isDirectory():
                    node = self.newFolder()
                    todo.append((node, level+1))
                else:
                    node = self.newNode()
                # insert the node in my contents and attach the file info in my vnodes table
                folder.contents[entry] = node
                self.attach(node=node, info=nodeInfo)

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
    def __init__(self, info, recognizer, walker, vnodes=None, **kwds):
        super().__init__(**kwds)

        # register the discovery mechanisms
        self.walker = walker
        self.recognizer = recognizer

        # storage for information about my nodes
        # if descendants provide a custom container, use it; otherwise use a weak dictionary
        # descendants must remember to override self.attach to match the custom container
        self.vnodes = vnodes or weakref.WeakKeyDictionary()

        # insert myself to the vnode table
        self.attach(node=self, info=info)

        return


# end of file 
