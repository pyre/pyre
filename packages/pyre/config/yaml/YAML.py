# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# my superclass
from ..Codec import Codec


# the configuration event generator
class YAML(Codec):
    """
    A reader/writer for yaml encoded configurations
    """

    # constants
    encoding = "yaml"

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
        # harvest the configuration events
        configuration = parser.parse(uri=uri, stream=source, locator=locator)
        # grab the accumulated errors
        errors = parser.errors
        # if there were no errors
        if not errors:
            # return the harvested configuration events
            return configuration
        # otherwise, throw away the harvested events
        return []


# end of file
