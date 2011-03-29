# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import weakref
from . import _metaclass_Node


class Node(metaclass=_metaclass_Node):
    """
    The base class for all filesystem entries
    
    Node and Folder are leaf and container nodes for the Composite that enables the
    representation of the hierarchical structure of filesystems
    """

    
    # constants
    from . import PATH_SEPARATOR


    # public data
    contents = {} # i don't have any, but some of my descendants do

    # properties
    @property
    def info(self):
        """
        Ask my filesystem to retrieve my information node
        """
        return self._filesystem().info(self)


    # interface
    @classmethod
    def join(cls, *fragments):
        """
        Concatenate the collection of path names in {paths} using the path separator.

        Absolute path names cause all previous path components to be discarded, just like
        {os.path.join}
        """
        # access the package utility
        from . import join
        # build the answer
        return join(*fragments)
            

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
