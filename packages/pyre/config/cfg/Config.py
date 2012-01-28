# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# my superclass
from ..Codec import Codec


# class declaration
class Config(Codec):
    """
    This package contains the implementation of the {cfg} reader and writer
    """


    # constants
    encoding = "cfg"


    # interface
    def decode(self, uri, source, locator):
        """
        Parse {source} and return the configuration events it contains
        """
        # make a parser
        from .Parser import Parser
        parser = Parser()
        # parse the contents of {source}
        try:
            # harvest the configuration events
            configuration = parser.parse(uri=uri, stream=source, locator=locator)
        # if anything goes wrong
        except parser.ParsingError as error:
            # build the error message parts
            msg = "decoding error in {}: {}".format(error.locator, error.description)
            # convert the parsing error into a decoding error and raise it
            raise self.DecodingError(codec=self, uri=uri, locator=error.locator, description=msg)

        # return the harvested configuration events
        return configuration


# end of file
