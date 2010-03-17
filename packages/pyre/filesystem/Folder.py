# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node


class Folder(Node):
    """
    The base class for containers of Nodes
    """

    # public data
    contents = None # the container that assigns names to my contents


    # interface
    def find(self, path):
        """
        Locate the entry with address {path}

        parameters:
            {path}: a PATH_SEPARATOR delimited chain of node names
        """
        # extract the list of path names
        names = filter(None, path.split(self.PATH_SEPARATOR))
        # initialize the lookup chain
        node = self
        # find the target node
        for name in names:
            node = node.contents[name]
        # and return it
        return node


    def insert(self, path, node):
        """
        Insert {vnode} at the location pointed to by {path}, creating all necessary
        intermediate directories
        """
        # extract the list of path names
        names = tuple(filter(None, path.split(self.PATH_SEPARATOR)))

        # we need to be careful here because one of the components of path may exist but not be
        # a folder, so we need to traverse the path once before we make any changes to the
        # folder layout

        # start out using myself as the target
        current = self
        # visit all folders in {path} and verify that the insertion will succeed
        for name in names[:-1]:
            # attempt to get the node pointed to by name
            try:
                current = current.contents[name]
            except KeyError:
                # it's ok for this to fail; we just have some nodes to make
                break
            # raise an exception if the current node is not a folder
            if not isinstance(current, Folder):
                from . import FolderError
                raise FolderError(self._filesystem, self, path, name)

        # if we get this far, all existing named nodes were folders
        # re-initialize the lookup chain
        current = self
        # find the  target node
        for name in names[:-1]:
            try:
                current = current.contents[name]
            except KeyError:
                folder = Folder(filesystem=self._filesystem())
                current.contents[name] = folder
                current = folder
        # add the node to the last directory
        current.contents[names[-1]] = node
        # and return it
        return node


    def mount(self, name, filesystem):
        """
        Make the root of {filesystem} available as {name} through my contents

        parameters:
            {name}: a string specifying the new name of the filesystem
            {filesystem}: the filesystem object whose root is being made available
        """
        # add the root node to my contents under the given name
        self.contents[name] = filesystem
        # and return it
        return self


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.contents = dict()
        return


    # access through subscripts
    def __getitem__(self, path):
        """
        Enable the sytax folder[{path}]
        """
        return self.find(path)


    def __setitem__(self, path, node):
        """
        Enable the syntax folder[{path}] = node
        """
        return self.insert(path=path, node=node)


    # constants
    from . import PATH_SEPARATOR


# end of file 
