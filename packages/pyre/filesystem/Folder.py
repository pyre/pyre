# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# base class
from .Node import Node


# declaration
class Folder(Node):
    """
    The base class for filesystem entries that are containers of other entries

    {Node} and {Folder} are the leaf and container types for the composite that enables the
    representation of the hierarchical structure of filesystems.
    """


    # constants
    isFolder = True


    # types
    # my metadata
    from .metadata import FolderInfo as metadata
    # exceptions
    from .exceptions import FolderInsertionError, FolderError, IsFolderError, NotFoundError


    # interface
    # searching for specific contents
    def find(self, pattern=None):
        """
        Generate pairs ({node}, {name}) that match the given pattern

        By default, {find} will create a generator that visits the entire contents of the tree
        rooted at this folder. In order to restrict the set of matching names, provide a
        regular expression as the optional argument {pattern}
        """
        # access the finder factory
        from . import finder
        # to build one
        f = finder()
        # and start the search
        return f.explore(folder=self, pattern=pattern)
        

    # populating filesystems
    def discover(self, **kwds):
        """
        Fill my contents by querying whatever external resource my filesystem represents
        """
        # punt to the implementation in my filesystem
        return self.filesystem().discover(root=self, **kwds)


    # making entire filesystems available through me
    def mount(self, uri, filesystem):
        """
        Make the root of {filesystem} available as {uri} within my filesystem
        """
        # easy enough: just insert {filesystem} at {uri}
        return self._insert(uri=uri, node=filesystem)


    # node factories
    def node(self):
        """
        Build a new node within my filesystem
        """
        # easy enough
        return Node(filesystem=self.filesystem())


    def folder(self):
        """
        Build a new folder within my filesystem
        """
        # also easy
        return Folder(filesystem=self.filesystem())


    # meta methods
    def __init__(self, **kwds):
        """
        Build a folder. See {pyre.filesystem.Node} for construction parameters
        """
        # chain up
        super().__init__(**kwds)
        # initialize my contents
        self.contents = {}
        # and return
        return
        

    def __getitem__(self, uri):
        """
        Retrieve a node given its {uri} as the subscript
        """
        # invoke the implementation and return the result
        return self._retrieve(uri)


    def __setitem__(self, uri, node):
        """
        Attach {node} at {uri}
        """
        # invoke the implementation and return the result
        return self._insert(node=node, uri=uri)


    def __contains__(self, uri):
        """
        Check whether {uri} is one of my children
        """
        # take the {uri} apart
        names = filter(None, uri.split(self.separator))
        # starting with me
        node = self
        # attempt to
        try:
            # iterate over the names
            for name in names: node = node.contents[name]
        # if node is not a folder, report failure
        except AttributeError: return False
        # if {name} is not among the contents of node, report failure
        except KeyError: return False
        # if we get this far, report success
        return True


    # implementation details
    def _retrieve(self, uri):
        """
        Locate the entry with address {uri}
        """
        # take {uri} apart
        names = filter(None, uri.split(self.separator))
        # starting with me
        node = self
        # attempt to
        try:
            # hunt down the target node
            for name in names: node = node.contents[name]
        # if any of the folder lookups fail
        except KeyError:
            # notify the caller
            raise self.NotFoundError(
                filesystem=self.filesystem(), node=self, uri=uri, fragment=name)
        # if one of the intermediate nodes is not a folder
        except AttributeError:
            # notify the caller
            raise self.FolderError(
                filesystem=self.filesystem(), node=self, uri=uri, fragment=node.uri)
        # otherwise, return the target node
        return node


    def _insert(self, node, uri, metadata=None):
        """
        Attach {node} at the address {uri}, creating all necessary intermediate folders.
        """
        # build the list of node names
        names = tuple(filter(None, uri.split(self.separator)))
        # keep track of the path fragment we have visited
        path = [self.uri]
        # starting with me
        current = self
        # visit all folders in {uri}
        for name in names[:-1]:
            # add {name} to the {path}
            path.append(name)
            # attempt to 
            try:
                # get the node pointed to by {name}
                current = current.contents[name]
            # if not there
            except KeyError:
                # no problem; let's make a folder
                folder = current.folder()
                # attach it
                current.contents[name] = folder
                # notify the filesystem
                self.filesystem().attach(node=folder, uri=self.join(*path))
                # and make it the current node
                current = folder
            # if it is there
            else:
                # check that it is a folder 
                if not current.isFolder:
                    # if not, raise an error
                    raise self.FolderInsertionError(
                        filesystem=self.filesystem(), node=self, uri=uri, target=name)

        # at this point, all intermediate folders have been processed
        # get the name of the node
        name = names[-1]
        # update the path
        path.append(name)
        # attach the node to its folder
        current.contents[names[-1]] = node
        # build the path of the node
        self.filesystem().attach(node=node, uri=self.join(*path), metadata=metadata)
        # and return it
        return node


    # private data
    __slots__ = 'contents',


# end of file 
