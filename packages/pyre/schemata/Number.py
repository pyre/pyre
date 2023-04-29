# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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
    # τ is a {3.6} feature
    try:
        # if it's there, pull it
        context["τ"] = math.tau
    # otherwise
    except AttributeError:
        # compute it
        context["τ"] = 2 * math.pi
    # all done
    return context


# declaration
class Number(Schema):
    """
    Intermediate class to mark the schemata that are numeric
    """

    # constants
    context = evaluationContext()


# end of file
