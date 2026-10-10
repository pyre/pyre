# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol of encoded images
class Image(pyre.flow.specification, family="pyre.viz.images"):
    """
    The image protocol: the encoded picture of a tile, ready to be shipped to a client
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default image
        """
        # use BMP as the default image
        from ..images.BMP import BMP

        # and return it
        return BMP


# end of file
