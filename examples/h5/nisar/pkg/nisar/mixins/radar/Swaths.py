# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
from nisar import h5

# the shared SLC pieces
from ..slc import frequency


# the radar-geometry imagery container
class Swaths(h5.schema.group):
    """
    The {swaths} group: imagery in radar (range-Doppler) geometry, by frequency

    Both frequency sub-bands are declared but marked optional; which ones are
    actually present in a given file is the per-file truth carried by the
    {listOfFrequencies} dataset in the product's identification group.
    """

    # the frequency sub-bands; both optional, presence driven by listOfFrequencies
    frequencyA = frequency(optional=True)
    frequencyA.doc = "the frequency A sub-band"

    frequencyB = frequency(optional=True)
    frequencyB.doc = "the frequency B sub-band"

    # the radar coordinate axes; one dimensional, extent free
    slantRange = h5.schema.array(schema=h5.schema.float(), shape=[...])
    slantRange.doc = "the slant range coordinates of the radar grid"

    zeroDopplerTime = h5.schema.array(schema=h5.schema.float(), shape=[...])
    zeroDopplerTime.doc = "the zero-Doppler azimuth time coordinates"


# end of file
