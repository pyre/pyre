# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
import nisar

# the band-level common pieces
from .Identification import Identification


# the base of every L-band NISAR product file
class LSAR(nisar.h5.schema.root, location="/science/LSAR"):
    """
    The base of every L-band (LSAR) NISAR product, rooted at /science/LSAR

    The {location} keyword mounts this group at its absolute path; products
    subclass {LSAR} and inherit the mount. The band-level {identification} lives
    here, as a sibling of the product group that each product adds. An analogous
    {SSAR} base, mounted at /science/SSAR, will host the S-band products once
    their structure is known; declaring the bands as separate bases (rather than
    as members of a shared {science} group) keeps the namespace open instead of
    contracting every file to carry both bands.
    """

    # the band-level identification, common to all L-band products
    identification = Identification()
    identification.doc = "the identification metadata"


# end of file
