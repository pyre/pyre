# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import zipfile
# support
from .. import primitives
# base class
from .Filesystem import Filesystem


# class declaration
class Zip(Filesystem):
    """
    Representation of a filesystem mounted from a zip file on the local host machine
    """


    # node metadata
    from .metadata import ZipNode, ZipFolder


    # interface
    def open(self, node, **kwds):
        """
        Open the file associate with {node}
        """
        # get the node metadata
        metadata = self.vnodes[node]
        # and call the {zipfile} file factory, which accepts {ZipInfo} instances as well as
        # archive data members
        return self.zipfile.open(metadata.zipinfo, **kwds)


    def discover(self, **kwds):
        """
        Populate the filesystem with the contents of the zipfile

        The current implementation does not allow the specification of the number of levels in
        the hierarchy to retrieve, mostly because the interface of the underlying zipfile
        object does not allow for efficient retrievals. This may change in a future
        implementation.
        """
        # get the archive contents
        for name, info in zip(self.zipfile.namelist(), self.zipfile.infolist()):
            # recognize the type of entry: directories end with a slash, everything else is a
            # file
            # start by converting the name into a path
            path = primitives.path(name)
            # so if the name ends with a slash
            if name[-1] == '/':
                # make folder
                node = self.folder()
                # build the metadata
                metadata = self.ZipFolder(uri=path, zipinfo=info)
            # otherwise
            else:
                # make a regular node
                node = self.node()
                # build the metadata
                metadata = self.ZipNode(uri=path, zipinfo=info)
            # insert the node
            self._insert(node=node, uri=path, metadata=metadata)
        # all done
        return self


    # meta methods
    def __init__(self, metadata, **kwds):
        # chain up
        super().__init__(metadata=metadata, **kwds)
        # create the zip file object for my archive
        self.zipfile = zipfile.ZipFile(str(metadata.uri))
        # and return
        return


    # private data
    __slots__ = 'zipfile',


# end of file
