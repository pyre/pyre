# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol of what a reader found in its file
class Contents(pyre.flow.specification, family="pyre.viz.contents"):
    """
    What a reader found in its file: the axes that tell its datasets apart, with the values each
    one may take, and the datasets themselves, each known by its value along every axis
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default way of holding the contents of a file
        """
        # in memory
        from ..contents.Memory import Memory

        # publish
        return Memory


# end of file
