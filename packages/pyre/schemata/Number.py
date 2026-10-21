# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import math

# superclass
from .Schema import Schema


# helper
def evaluationContext():
    """
    Build an evaluation context
    """
    # initialize an empty one
    context = {}
    # push {math} in my context
    context.update(math.__dict__)
    # enable the greek letters for the corresponding constants
    context["π"] = math.pi
    # both of them
    context["τ"] = math.tau
    # all done
    return context


# declaration
class Number(Schema):
    """
    Intermediate class to mark the schemata that are numeric
    """

    # constants
    context = evaluationContext()

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a number
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onNumber
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)


# end of file
