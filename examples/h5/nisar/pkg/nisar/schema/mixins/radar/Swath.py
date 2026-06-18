# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import nisar

# the datum
from ...descriptors import slc


# a frequency sub-band of single-look-complex imagery in radar geometry
class Swath(nisar.h5.schema.group):
    """
    A frequency sub-band of single-look-complex imagery, in radar (range-Doppler) geometry

    Contained by the {Swaths} group. Provides the per-frequency range dimension and carries
    the SLC channels and the slant-range coordinate axis. The azimuth dimension is shared
    across the swath's frequencies and lives on {Swaths}.
    """

    # the range dimension, scoped to this sub-band
    nsamples = nisar.h5.schema.dimension()
    nsamples.doc = "the number of slant-range samples"

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

    # the slant-range coordinate axis: one value per sample
    slantRange = nisar.h5.schema.array(schema=nisar.h5.schema.float(), shape=["nsamples"])
    slantRange.doc = "the slant range coordinates of the radar grid"


# end of file
