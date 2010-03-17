# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node
from .Folder import Folder
from . import _metaclass_Filesystem


class Filesystem(Folder, metaclass=_metaclass_Filesystem):
    """
    The base class for representing filesystems
    """


    def createFolder(self, path):
        """
        Create a node and insert it at the location pointed to by {path}
        """
        # create the node
        node = Folder(filesystem=self)
        # add it to my contents
        self[path] = node
        # and return it
        return node


    def createNode(self, path):
        """
        Create a node and insert it at the location pointed to by {path}
        """
        # create the node
        node = Node(filesystem=self)
        # add it to my contents
        self[path] = node
        # and return it
        return node


    def __init__(self, **kwds):
        super().__init__(filesystem=self, **kwds)
        return


# end of file 
