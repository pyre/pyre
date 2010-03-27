# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#



from ..Codec import Codec


class PML(Codec):
    """
    This package contains the implementation of the pml reader and writer
    """


    # constants
    encoding = "pml"


    # interface
    def decode(self, stream):
        """
        Parse {stream} and return its contents
        """
        # get access to the XML package
        import pyre.xml
        # and the pml document
        from .Document import Document
        # make a reader
        reader = pyre.xml.newReader()
        # parse the contents
        item = reader.read(stream=stream, document=Document())
        # and return it
        return item


# end of file
