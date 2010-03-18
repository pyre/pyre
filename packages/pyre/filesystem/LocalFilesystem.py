# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Filesystem import Filesystem


class LocalFilesystem(Filesystem):
    """
    Encapsulation of a filesystem local to the machine on which the application is runing

    LocalFilsystem uses listdir, (l)stat and other C library routines appropriate for locally
    mounted filesystems to discover and serve its contents
    """


    # public data
    @property
    def mountpoint(self):
        return self.vnodes[self].uri


    # interface
    def sync(self):
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
    def __init__(self, root, info, recognizer, walker, vnodes=None, **kwds):
        super().__init__(**kwds)

        # storage for information about my nodes
        # if descendants provide a custom container, use it; otherwise use a dictionary
        # descendants must remember to override self.attach to match the custom container
        self.vnodes = vnodes or dict()

        # insert myself to the vnode table
        self.attach(node=self, info=info)

        return


# end of file 
