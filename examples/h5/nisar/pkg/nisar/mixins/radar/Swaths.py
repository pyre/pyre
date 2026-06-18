# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
import nisar

# the shared SLC pieces
from ..slc import frequency


# the radar-geometry imagery container
class Swaths(nisar.h5.schema.group):
    """
    The {swaths} group: imagery in radar (range-Doppler) geometry, by frequency

    Both frequency sub-bands are declared but marked optional; the {listOfFrequencies}
    dataset in the {identification} group indicates which ones are present
    """

    # the frequency sub-bands; both optional, presence driven by listOfFrequencies
    frequencyA = frequency(optional=True)
    frequencyA.doc = "the primary instrument band"

    frequencyB = frequency(optional=True)
    frequencyB.doc = "the secondary instrument band"

    # the radar coordinate axes; one dimensional, extent free
    slantRange = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=[...])
    slantRange.doc = "the slant range coordinates of the radar grid"

    zeroDopplerTime = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=[...])
    zeroDopplerTime.doc = "the zero-Doppler azimuth time coordinates"


# end of file
