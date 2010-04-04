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
    def decode(self, configurator, stream):
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
        try:
            configuration = reader.read(stream=stream, document=Document())
        except reader.ParsingError as error:
            locator = error.locator
            source = locator.source
            msg = "decoding error in {}: {}".format(locator, error.description)
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=msg) from error

        # record the harvested events
        # the assignments
        for key,value in configuration.bindings:
            configurator.createAssignment(key, value)
        # and return the configuration
        return configuration


# end of file
