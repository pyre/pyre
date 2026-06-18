# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import nisar

# the per-frequency radar imagery group
from .Swath import Swath as swath


# the radar-geometry imagery container
class Swaths(nisar.h5.schema.group):
    """
    The {swaths} group: imagery in radar (range-Doppler) geometry, by frequency

    Provides the azimuth dimension shared across this swath's frequencies. Both frequency
    sub-bands are declared but marked optional; the {listOfFrequencies} dataset in the
    {identification} group indicates which ones are present.
    """

    # the azimuth dimension, shared by this swath's frequencies
    nlines = nisar.h5.schema.dimension()
    nlines.doc = "the number of zero-Doppler azimuth lines"

    # the frequency sub-bands; both optional
    frequencyA = swath(optional=True)
    frequencyA.doc = "the primary instrument band"

    frequencyB = swath(optional=True)
    frequencyB.doc = "the secondary instrument band"

    # the azimuth coordinate axis: one value per line
    zeroDopplerTime = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=["nlines"])
    zeroDopplerTime.doc = "the zero-Doppler azimuth time coordinates"


# end of file
