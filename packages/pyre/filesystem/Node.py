# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
from . import _metaclass_Node


class Node(metaclass=_metaclass_Node):
    """
    The base class for all filesystem entries
    
    Node and Folder are leaf and container nodes for the Composite that enables the
    representation of the hierarchical structure of filesystems
    """

    
    # public data
    contents = {} # i don't have any, but some of my descendants do


    # interface
    def open(self, **kwds):
        """
        Access the contents of the physical resource that i point to.
        """
        # delegate the action to the containing filesystem
        return self._filesystem().open(self, **kwds)


    # explorer support
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a node
        """
        return explorer.onNode(self, **kwds)


    # meta methods
    def __init__(self, filesystem, **kwds):
        super().__init__(**kwds)
        self._filesystem = weakref.ref(filesystem)
        return


# end of file 
