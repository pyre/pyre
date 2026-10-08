# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Real import Real


# a refinement of the real specification
class Unit(Real, family="pyre.viz.tiles.unit"):
    """
    The specification of tiles of real values in [0,1], such as the output of a normalizer
    """


# end of file
