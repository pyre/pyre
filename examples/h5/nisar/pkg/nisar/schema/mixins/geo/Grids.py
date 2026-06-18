# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import nisar

# the per-frequency geocoded imagery group
from .Grid import Grid as grid


# the geocoded imagery container
class Grids(nisar.h5.schema.group):
    """
    The {grids} group: imagery on a map projection grid, by frequency

    Both frequency sub-bands are declared but marked optional; the {listOfFrequencies}
    dataset in the {identification} group indicates which ones are present.
    """

    # the frequency sub-bands; both optional
    frequencyA = grid(optional=True)
    frequencyA.doc = "the primary instrument band"

    frequencyB = grid(optional=True)
    frequencyB.doc = "the secondary instrument band"


# end of file
