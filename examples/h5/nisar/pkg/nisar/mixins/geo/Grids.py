# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
import nisar

# the shared SLC pieces
from ..slc import frequency


# the geocoded imagery container
class Grids(nisar.h5.schema.group):
    """
    The {grids} group: imagery on a map projection grid, by frequency

    Both frequency sub-bands are declared but marked optional; which ones are
    actually present in a given file is the per-file truth carried by the
    {listOfFrequencies} dataset in the product's identification group.
    """

    # the frequency sub-bands; both optional, presence driven by listOfFrequencies
    frequencyA = frequency(optional=True)
    frequencyA.doc = "the frequency A sub-band"

    frequencyB = frequency(optional=True)
    frequencyB.doc = "the frequency B sub-band"

    # the map projection coordinate axes; one dimensional, extent free
    xCoordinates = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=[...])
    xCoordinates.doc = "the projected x (easting) coordinates of the map grid"

    yCoordinates = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=[...])
    yCoordinates.doc = "the projected y (northing) coordinates of the map grid"


# end of file
