# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Folder(Node):
    """
    The base class for containers of Nodes
    """

    # public data
    # constants
    from . import PATH_SEPARATOR
    
    # data members
    contents = None # the container that assigns names to my contents

    @property
    def mountpoint(self):
        """
        My location
        """
        return self._filesystem().info(self).uri


    # types
    # exceptions
    from .exceptions import FolderInsertionError, NotFoundError


    # interface
    def explore(self, **kwds):
        """
        Ask my filesystem to populate me
        """
        return self._filesystem().sync(root=self, **kwds)


    def find(self, **kwds):
        """
        Generate the list of names that match the given {pattern}

        By default, find will create a generator that visits the entire contents of the tree
        rooted at this folder. Use the optional arguments to restrict the set of matching
        names. For details about supported filters, see pyre.filesystem.Finder.
        """
        # get the finder factory
        from . import newFinder
        # build one 
        finder = newFinder()
        # get it to find what the user wants
        for (node, path) in finder.explore(folder=self, **kwds):
            yield (node, path)
        # all done
        return
        

    # populating filesystems
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


    # content factories
    def newFolder(self):
        """
        Create a new folder
        """
        # create the node
        return Folder(filesystem=self._filesystem())


    def newNode(self):
        """
        Create a new node
        """
        # create the node
        return Node(filesystem=self._filesystem())


    # explorer support
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a folder
        """
        return explorer.onFolder(self, **kwds)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.contents = dict()
        return


    # implementation details
    def _insert(self, node, path):
        """
        Insert {node} at the location pointed to by {path}, creating all necessary
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
                raise self.FolderInsertionError(
                    filesystem=self._filesystem(), node=self, path=path, target=name)

        # if we get this far, all existing named nodes were folders
        # re-initialize the lookup chain
        current = self
        # find the  target node
        for name in names[:-1]:
            try:
                current = current.contents[name]
            except KeyError:
                folder = current.newFolder()
                current.contents[name] = folder
                current = folder
        # add the node to the last directory
        current.contents[names[-1]] = node
        # and return it
        return node


    def _find(self, path):
        """
        Locate the entry with address {path}

        parameters:
            {path}: a PATH_SEPARATOR delimited chain of node names

        Note: this method is the workhorse behind subscripted access to the folder contents and
        should probably not be used directly
        """
        # extract the list of path names
        names = filter(None, path.split(self.PATH_SEPARATOR))
        # initialize the lookup chain
        node = self
        # find the target node
        try:
            for name in names:
                node = node.contents[name]
        except KeyError:
            raise self.NotFoundError(
                filesystem=self._filesystem(), node=self, path=path, fragment=name)
        # and return it
        return node


    # access through subscripts
    def __getitem__(self, path):
        """
        Enable the syntax folder[{path}]
        """
        return self._find(path)


    def __setitem__(self, path, node):
        """
        Enable the syntax folder[{path}] = node
        """
        return self._insert(path=path, node=node)


    # debugging support
    def dump(self, interactive=True):
        """
        Print out my contents using a tree explorer
        """
        # build the explorer
        from . import newTreeExplorer
        explorer = newTreeExplorer()
        # get the representation of my contents
        printout = explorer.explore(self)
        # dump it out
        if interactive:
            for line in printout:
                print(line)
        # and return the explorer to the caller
        return explorer


# end of file 
