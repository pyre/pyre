# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os # for the path utilities
import time # for my timestamps
# base class
from .Filesystem import Filesystem


# class declaration
class Local(Filesystem):
    """
    An encapsulation of a filesystem mounted directly on the local host machine
    """


    # exceptions
    from .exceptions import DirectoryListingError


    # public data
    walker = None # the directory listing mechanism
    recognizer = None # the file type recognizer


    # interface
    def open(self, node, **kwds):
        """
        Open the file associated with {node}
        """
        # get the info record associated with the node and extract the file uri
        uri = self.vnodes[node].uri
        # call the system {open} and return the result
        return open(uri, **kwds)


    def make(self, name, tree, root=None, **kwds):
        """
        Duplicate the hierarchical structure in {tree} within my context
        """
        # print(" ** pyre.filesystem.Local.make:")
        # create a timestamp
        timestamp = time.gmtime()
        # adjust the location of the new branch
        root = root if root is not None else self
        # print(" ++ input:")
        # print("      root: {}".format(root))
        # print("      uri: {!r}".format(root.uri))
        # print("      tree: {!r}".format(tree.uri))

        # initialize the worklist
        todo = [ (root, name, tree) ]
        # print(" ++ adding:")
        # as long as there is more to do
        for parent, name, source in todo:
            # build the folder
            folder = parent.folder()
            # assemble the folder uri
            uri = self.join(parent.uri, name)
            # print("      {!r}".format(uri))

            # create the folder
            os.mkdir(uri)
            # build the node meta data
            meta = self.recognizer.recognize(uri)
            # insert the new node in the parent folder
            parent.contents[name] = folder
            # and update my vnode table
            self.vnodes[folder] = meta

            # add the children to my work list
            todo.extend( 
                (folder, name, child)
                for name, child in source.contents.items()
                # NYI: don't know how to handle regular files just yet; must take into account
                # the meta data associated with {node} in whatever filesystem {tree} came from,
                # just in case I am ever asked to build pipes and sockets and stuff... skip for
                # now.
                if child.isFolder )

        return tree


    def discover(self, root=None, walker=None, recognizer=None, levels=None):
        """
        Traverse the local filesystem starting with {root} and refresh my contents so that they
        match the underlying filesystem
        """
        # print(" ** pyre.filesystem.Local")
        # print("  input:")
        # print("    root: {!r}".format(root))
        # print("    levels: {!r}".format(levels))
        # print("  visiting:")
        # create a timestamp
        timestamp = time.gmtime()
        # use the supplied traversal support, if available
        walker = walker if walker is not None else self.walker
        recognizer = recognizer if recognizer is not None else self.recognizer
        # establish the starting point
        root = root if root is not None else self
        # print("    root uri: {!r}".format(root.uri))
        # make sure {root} is a folder
        if not root.isFolder:
            # otherwise complain
            raise self.DirectoryListingError(uri=root.uri, error='not a directory')
        # clear out the contents of {root}
        root.contents = {}
        # print("    before uri: {!r}".format(self.vnodes[root].uri))
        # initialize the traversal
        todo = [ (root, 0) ]
        # start walking and recognizing
        for folder, level in todo:
            # should we process this entry?
            if levels is not None and level >= levels: continue
            # compute the actual location of this directory
            location = self.vnodes[folder].uri
            # print("    uri: {!r}".format(location))
            # walk through the contents
            for entry in walker.walk(location):
                # build the absolute path of the entry
                address = os.path.join(location, entry)
                # recognize the file
                meta = recognizer.recognize(address)
                # time stamp it
                meta.syncTime = timestamp
                # if this is a directory
                if meta.isDirectory:
                    # build a new folder
                    node = self.folder()
                    # add this location to the {todo} list
                    todo.append( (node, level+1) )
                # otherwise
                else:
                    # build a regular node
                    node = self.node()
                # insert the new node in the parent folder
                folder.contents[entry] = node
                # and update my vnode table
                self.vnodes[node] = meta
        # all done
        # print("    after uri: {!r}".format(self.vnodes[root].uri))
        return root


    # meta methods
    def __init__(self, walker, recognizer, **kwds):
        super().__init__(**kwds)
        # attach the content discovery mechanisms
        self.walker = walker
        self.recognizer = recognizer

        return


# end of file 
