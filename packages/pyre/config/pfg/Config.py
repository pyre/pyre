# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from ..Codec import Codec


# class declaration
class Config(Codec):
    """
    This package contains the implementation of the {pfg} reader and writer
    """

    # constants
    encoding = "pfg"

    # interface
    @classmethod
    def decode(cls, uri, source, locator):
        """
        Parse {source} and return the configuration events it contains
        """
        # get the parser factory
        from .Parser import Parser

        # make a parser
        parser = Parser()
        # harvest all the configuration events, so the parser has seen the whole source
        configuration = list(parser.parse(uri=uri, stream=source, locator=locator))
        # if the parser ran into trouble
        if parser.errors:
            # throw away the harvested events, and complain
            raise cls.DecodingError(codec=cls, uri=uri, locator=locator, errors=parser.errors)
        # otherwise, return the harvested configuration events
        return configuration


# end of file
