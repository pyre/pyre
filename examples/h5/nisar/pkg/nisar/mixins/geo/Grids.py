# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
from nisar import h5

# the shared SLC pieces
from ..slc import frequency


# the geocoded imagery container
class Grids(h5.schema.group):
    """
    The {grids} group: imagery on a map projection grid, by frequency

    Both frequency sub-bands are declared but marked optional; which ones are
    actually present in a given file is the per-file truth carried by the
    {listOfFrequencies} dataset in the product's identification group.
    """

    # the frequency sub-bands; both optional, presence driven by listOfFrequencies
    frequencyA = frequency(optional=True)
    frequencyA.__doc__ = "the frequency A sub-band"

    frequencyB = frequency(optional=True)
    frequencyB.__doc__ = "the frequency B sub-band"

    # the map projection coordinate axes; one dimensional, extent free
    xCoordinates = h5.schema.array(schema=h5.schema.float(), shape=[...])
    xCoordinates.__doc__ = "the projected x (easting) coordinates of the map grid"

    yCoordinates = h5.schema.array(schema=h5.schema.float(), shape=[...])
    yCoordinates.__doc__ = "the projected y (northing) coordinates of the map grid"


# end of file
