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
    @classmethod
    def decode(cls, uri, source, locator):
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
            msg = "{{0.codec.encoding}} parsing error: {}".format(
                error.description)
            # convert the parsing error into a decoding error and raise it
            raise cls.DecodingError(codec=cls, uri=uri, locator=error.locator, description=msg)

        # return the harvested configuration events
        # for event in configuration: print(event)
        return configuration


# end of file
