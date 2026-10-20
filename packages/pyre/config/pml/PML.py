# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


from ..Codec import Codec


class PML(Codec):
    """
    This package contains the implementation of the pml reader and writer
    """

    # constants
    encoding = "pml"

    # interface
    @classmethod
    def decode(cls, uri, source, locator):
        """
        Parse {source} and return its contents
        """
        # get access to the XML package
        import pyre.xml

        # and the pml document
        from .Document import Document

        # make a reader
        reader = pyre.xml.newReader()
        # parse the contents
        try:
            # harvest the configuration events in the source
            configuration = reader.read(stream=source, document=Document())
        # if the reader ran into trouble
        except reader.ParsingError as error:
            # place it after the reason the source was read, if there is one
            if locator:
                # by chaining the two
                error.locator = pyre.tracking.chain(this=error.locator, next=locator)
            # throw away the harvested events, and complain
            raise cls.DecodingError(codec=cls, uri=uri, locator=locator, errors=[error]) from error
        # all done; return the harvested events
        # for event in configuration: print(event)
        return configuration


# end of file
