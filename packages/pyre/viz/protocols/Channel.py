# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Unit import Unit


# a refinement of the unit specification
class Channel(Unit, family="pyre.viz.tiles.channel"):
    """
    The specification of tiles that hold the intensity of one color primary, in [0,1]
    """


# end of file
