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
    def decode(self, configurator, stream, locator=None):
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
            if locator:
                loc = pyre.tracking.chain(this=error.locator, next=locator)
            else:
                loc = error.locator
            source = error.locator.source
            msg = "decoding error in {}: {}".format(loc, error.description)
            raise self.DecodingError(
                codec=self, uri=source, locator=loc, description=msg) from error

        # record the harvested events
        # the assignments
        for key,value,loc in configuration.bindings:
            # chain to the external locator, if available
            if locator:
                loc = pyre.tracking.chain(this=loc, next=locator)
            # record the event
            configurator.recordAssignment(key, value, loc)
        # and return the configuration
        return configuration


# end of file
