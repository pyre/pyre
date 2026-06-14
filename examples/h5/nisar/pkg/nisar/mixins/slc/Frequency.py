# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
from nisar import h5, constraints

# the datum
from .SLC import SLC


# a frequency sub-band of single-look-complex imagery
class Frequency(h5.schema.group):
    """
    A single frequency sub-band of single-look-complex imagery

    Shared by the SLC product family: each polarization channel is an {SLC}
    datum. The set actually present is mode dependent and is reported by
    {listOfPolarizations}.

    NOTE: this name is provisional; a better one is wanted.
    """

    # the polarizations carried by this sub-band; a non-empty subset of the four channels
    listOfPolarizations = h5.schema.strings()
    listOfPolarizations.constraints = [
        constraints.isSubset(choices={"HH", "HV", "VH", "VV"}),
        constraints.isNotEmpty(),
    ]
    listOfPolarizations.__doc__ = "the polarizations present in this frequency"

    # the channels; all optional, presence driven by listOfPolarizations
    # the co-polarized channels
    HH = SLC(optional=True)
    HH.__doc__ = "the HH polarization"

    VV = SLC(optional=True)
    VV.__doc__ = "the VV polarization"

    # the cross-polarized channels
    HV = SLC(optional=True)
    HV.__doc__ = "the HV polarization"

    VH = SLC(optional=True)
    VH.__doc__ = "the VH polarization"


# end of file
