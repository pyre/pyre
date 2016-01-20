# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import weakref # for {vnodes}, the weak key dictionary
# support
from .. import primitives
# base class
from .Folder import Folder


# declaration
class Filesystem(Folder):
    """
    The base class for representing filesystems

    A filesystem is a special {Folder} that maintains an association between the {Nodes} it
    contains and {Info} objects that are dependent on the specific filesystem type and capture
    what the filesystem knows about them.
    """


    # exceptions
    from .exceptions import NotFoundError, SourceNotFoundError, URISpecificationError, FolderError


    # interface
    def info(self, node):
        """
        Look up and return the available metadata associated with {node}
        """
        # let the exceptions through, for now
        return self.vnodes[node]


    def open(self, node, **kwds):
        """
        Open the file associated with {node}
        """
        # i don't know how to do it
        raise NotImplementedError(
            "class {.__name__!r} must implement 'open'".format(type(self)))


    def getFolder(self, *args):
        """
        Assemble a path by joining {args} together and return the folder at that location. If the
        folder does not exist, create it and mount it
        """
        # make the path
        path = primitives.path(*args)
        # attempt to
        try:
            # get the node at the specified location
            target = self[path]
        # if not
        except self.NotFoundError:
            # make it
            target = self.folder()
            # and mount it
            self[path] = target
        # if the folder exists
        else:
            # check that the {target} is a folder
            if not target.isFolder:
                # and if not, complain
                raise self.FolderError(uri=path, fragment=path, filesystem=self, node=target)

        # otherwise, all good
        return target


    # implementation details
    def attach(self, node, uri, metadata=None, **kwds):
        """
        Maintenance for the {vnode} table. Filesystems that maintain more elaborate metadata
        about their nodes must override to build their info structures.
        """
        # if we were not handed any node metadata
        if metadata is None:
            # build a node specific {info} structure
            metadata = node.metadata(uri=uri, **kwds)
        # otherwise
        else:
            # decorate the given structure
            metadata.uri = uri
        # attach it to my vnode table
        self.vnodes[node] = metadata
        # and return it
        return metadata


    # meta methods
    def __init__(self, metadata=None, **kwds):
        # chain up to make me a valid node with me as the filesystem
        super().__init__(filesystem=self, **kwds)
        # my vnode table: a map from nodes to info structures
        self.vnodes = weakref.WeakKeyDictionary()
        # build an info structure for myself
        metadata = self.metadata(uri=primitives.path('/')) if metadata is None else metadata
        # add it to my vnode table
        self.vnodes[self] = metadata
        # all done
        return


    # implementation details
    __slots__ = ('vnodes')


# end of file
