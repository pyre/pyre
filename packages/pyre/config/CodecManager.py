# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import collections


class CodecManager:
    """
    The manager of the known reader/writers of the various configuration file formats.

    The pyre executive uses a CodecManager instance to gain access to the default processors
    and to simplify extending support to user provided formats, which can be made available to
    the framework by registering them with the code manager
    """


    # interface
    def newCodec(self, encoding, **kwds):
        """
        Retrieve the factory associated with the given encoding and build a codec instance
        """
        return self.codecs[encoding](**kwds)


    def register(self, encoding, codec):
        """
        Add the {codec} for the file format {encoding} to the index

        The encoding typically correponds to both the method porrtion of a URI, as well as specify
        the extension of local files in this format
        """
        self.codecs[encoding] = codec
        return self


    def getEncodings(self):
        """
        Return the registered encodings
        """
        return self.codecs.keys()


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.codecs = self._indexDefaultCodecs()
        return


    # implementation details
    def _indexDefaultCodecs(self):
        """
        Initialize the codec index with the default file handlers
        """
        index = collections.OrderedDict()

        # the odb file handler
        from .odb.ODB import ODB
        index[ODB.encoding] = index["vfs"] = index["file"] = ODB


        # the pml file handler
        from .pml.PML import PML
        index[PML.encoding] = PML

        # the pcs file handler
        from .pcs.PCS import PCS
        index[PCS.encoding] = PCS

        # importing from packages on the python path
        from .native.Importer import Importer
        index[Importer.encoding] = Importer

        # all done
        return index


# end of file
