# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# framework
from ..traits.Property import Property

# the schema for a single requirement
from .RequirementSchema import RequirementSchema


# the trait descriptor for a single requirement, assembled from the same pedigree the
# {schemata.typed} decorator uses to build the standard typed properties
class RequirementProperty(Property.schema, Property, RequirementSchema):
    """
    A trait descriptor for a single package requirement
    """


# end of file
