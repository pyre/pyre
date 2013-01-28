# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import weakref
# my metaclass
from . import _metaclass_Node


# declaration
class Node(metaclass=_metaclass_Node):
    """
    The base class for all filesystem entries

    {Node} and {Folder} are the leaf and container types for the composite that enables the
    representation of the hierarchical structure of filesystems.
    """


    # constants
    isFolder = False
    from . import separator


    # types
    # my metadata
    from .metadata import NodeInfo as metadata
    # exceptions
    from .exceptions import GenericError


    # public data
    @property
    def uri(self):
        """
        Return my location relative to the root of my filesystem
        """
        # this much is guaranteed to exist for all well-formed filesystems
        return self.filesystem().info(node=self).uri


    @property
    def marker(self):
        """
        Return my distinguishing mark used by explorers to decorate their reports
        """
        # this much is guaranteed to exist for all well-formed filesystems
        return self.filesystem().info(node=self).marker


    # interface
    @classmethod
    def join(cls, *paths, separator=None):
        """
        Concatenate the collection of path names in {paths} using the path separator.

        Absolute path names cause all previous path components to be discarded, just like
        {os.path.join}
        """
        # initialize the separator
        if separator is None: separator = cls.separator
        # prime the result
        fragments = []
        # iterate over the given names
        for path in paths:
            # disregard empty path fragments
            if not path: continue
            # discard the current state if this is an absolute path
            if path[0] == separator: fragments = []
            # convert a lone separator into an empty fragment
            if path == separator: path = ''
            # add this path to the pile
            fragments.append(path)
        # assemble the answer
        return separator.join(fragments)


    def open(self, **kwds):
        """
        Access the contents of the physical resource with which I am associated
        """
        # delegate the action to the filesystem
        return self.filesystem().open(node=self, **kwds)


    # meta methods
    def __init__(self, filesystem, **kwds):
        """
        Build a node:
            filesystem: one of the supported filesystems
        """
        # chain up
        super().__init__(**kwds)
        # build a weak reference to my filesystem
        self.filesystem = weakref.ref(filesystem)
        # and return
        return


    # implementation details
    __slots__ = '__weakref__', 'filesystem'


    # debugging support
    def dump(self, interactive=True, indent=''):
        """
        Print out my contents using a tree explorer
        """
        # bail out if not in interactive mode
        if not interactive: return self

        # build an explorer
        from . import treeExplorer
        explorer = treeExplorer()
        # get the representation of my contents and dump it out
        for line in explorer.explore(node=self, label=self.uri): print("{}{}".format(indent, line))
        # all done
        return self


# end of file 
