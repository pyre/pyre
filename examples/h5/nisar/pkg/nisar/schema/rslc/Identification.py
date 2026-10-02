# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
import nisar

# the base identification group
from ..mixins.common import identification


# the identification group specialized for the RSLC product
class Identification(identification):
    """
    The identification metadata for an RSLC product

    Redeclares {productType} locally and fixes its default to the value for this
    product type; the descriptor is rebuilt rather than mutated in place, since
    the inherited one is a shared class attribute.
    """

    # the product type is fixed for RSLC
    productType = nisar.h5.schema.str()
    productType.default = "RSLC"
    productType.doc = "the product type, fixed for RSLC"


# end of file
