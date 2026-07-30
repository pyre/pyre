# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# framework
from .. import schemata

# the requirement value class
from .Requirement import Requirement


# the schema for a single requirement
class RequirementSchema(schemata.identity):
    """
    A type declarator for package requirements

    Values pass through {Requirement.parse}, so traits with this schema accept both text
    specifications and structured requirements, and always hand back the structured form
    """

    # constants
    typename = "requirement"  # the name of my type
    complaint = "could not coerce {0.value!r} into a requirement"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a requirement
        """
        # only text and structured requirements are candidates
        if not isinstance(value, (str, Requirement)):
            # anything else is unusable
            raise self.CastingError(value=value, description=self.complaint)
        # attempt to
        try:
            # push the value through the parser; structured requirements pass through
            return Requirement.parse(spec=value)
        # if the specification is malformed
        except Requirement.RequirementSyntaxError as error:
            # convert the complaint into the type system's vocabulary
            raise self.CastingError(value=value, description=str(error)) from error

    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
