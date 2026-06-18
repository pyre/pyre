# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import nisar

# the datum
from ...descriptors import slc


# a frequency sub-band of single-look-complex imagery on a map projection grid
class Grid(nisar.h5.schema.group):
    """
    A frequency sub-band of single-look-complex imagery, on a map projection grid

    Contained by the {Grids} group. In geocoded geometry both grid extents are
    per-frequency, so this group provides both shape dimensions and carries the SLC channels
    and the projected coordinate axes.
    """

    # both grid extents are per-frequency in geocoded geometry
    nlines = nisar.h5.schema.dimension()
    nlines.doc = "the number of rows, the y extent of the grid"

    nsamples = nisar.h5.schema.dimension()
    nsamples.doc = "the number of columns, the x extent of the grid"

    # the polarizations carried by this sub-band; a non-empty subset of the four channels
    listOfPolarizations = nisar.h5.schema.strings()
    listOfPolarizations.constraints = [
        nisar.constraints.isSubset(choices={"HH", "HV", "VH", "VV"}),
        nisar.constraints.isNotEmpty(),
    ]
    listOfPolarizations.doc = "the polarizations present in this frequency"

    # the channels; all optional, presence driven by listOfPolarizations
    HH = slc(optional=True)
    HH.doc = "the HH polarization"

    VV = slc(optional=True)
    VV.doc = "the VV polarization"

    HV = slc(optional=True)
    HV.doc = "the HV polarization"

    VH = slc(optional=True)
    VH.doc = "the VH polarization"

    # the map-projection coordinate axes, one value per grid point along each axis
    xCoordinates = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=["nsamples"])
    xCoordinates.doc = "the projected x (easting) coordinates of the map grid"

    yCoordinates = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=["nlines"])
    yCoordinates.doc = "the projected y (northing) coordinates of the map grid"


# end of file
