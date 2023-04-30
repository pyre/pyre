# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# get the framework
import pyre


# the base class for my exceptions
class MerlinError(pyre.PyreError):
    """
    Base class for all merlin errors
    """


class UnrecognizableSourceLanguageError(MerlinError):
    """
    Exception raised when the source language of an asset could not be recognized
    """

    # public data
    description = "{0.node.uri}: could not determine the source language"

    # meta methods
    def __init__(self, node, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the node
        self.node = node
        # all done
        return


# end of file
