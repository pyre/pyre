# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Real import Real


# a refinement of the real specification
class Magnitude(Real, family="pyre.viz.tiles.magnitude"):
    """
    The specification of tiles of magnitudes: real values that are never negative, such as the modulus of complex samples
    """


# end of file
