# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
from nisar import h5, constraints


# the identification group
class Identification(h5.schema.group):
    """
    The metadata that identifies a NISAR data product; present in every product

    Individual products derive their own local subclass to nail down and freeze
    the fields that are fixed for that product type (see e.g. the product-local
    {Identification} subclasses under {products/rslc} and {products/gslc}). When a
    field is specialized, the descriptor is redeclared locally rather than mutated
    in place, since the inherited descriptor is a shared class attribute.
    """

    # the mission that produced the data; fixed for the whole program
    missionId = h5.schema.str()
    missionId.default = "NISAR"
    missionId.__doc__ = "the name of the mission"

    # the kind of product; products fix this in their own subclass
    productType = h5.schema.str()
    productType.__doc__ = "the type of the data product"

    # the version of the product specification
    productVersion = h5.schema.str()
    productVersion.__doc__ = "the version of the data product specification"

    # the frequency sub-bands carried by this product; a non-empty subset of {"A", "B"}
    listOfFrequencies = h5.schema.strings()
    listOfFrequencies.constraints = [
        constraints.isSubset(choices={"A", "B"}),
        constraints.isNotEmpty(),
    ]
    listOfFrequencies.__doc__ = "the frequency sub-bands present in this product; from {'A', 'B'}"

    # the orbit
    absoluteOrbitNumber = h5.schema.int()
    absoluteOrbitNumber.__doc__ = "the absolute orbit number"

    # the track
    trackNumber = h5.schema.int()
    trackNumber.__doc__ = "the track number"

    # the frame
    frameNumber = h5.schema.int()
    frameNumber.__doc__ = "the frame number"

    # the antenna pointing
    lookDirection = h5.schema.str()
    lookDirection.__doc__ = "the look direction: 'left' or 'right'"

    # the direction of travel
    orbitPassDirection = h5.schema.str()
    orbitPassDirection.__doc__ = "the orbit pass direction: 'ascending' or 'descending'"


# end of file
