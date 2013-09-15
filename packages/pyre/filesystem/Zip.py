# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import zipfile
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
            if name[-1] == '/':
                node = self.folder()
                metadata = self.ZipFolder(uri=name, zipinfo=info)
            else: 
                node = self.node()
                metadata = self.ZipNode(uri=name, zipinfo=info)
            # insert the node
            self._insert(node=node, uri=name, metadata=metadata)
        # all done
        return self

    
    # meta methods
    def __init__(self, metadata, **kwds):
        super().__init__(metadata=metadata, **kwds)
        # create the zip file object for my archive
        self.zipfile = zipfile.ZipFile(metadata.uri)
        # and return
        return


    # private data
    __slots__ = 'zipfile',


# end of file 
