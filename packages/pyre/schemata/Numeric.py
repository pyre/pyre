# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .Schema import Schema


# helper
def evaluationContext():
    """
    Build an evaluation context
    """
    # initialize an empty one
    context = {}

    # load the math module
    import math
    # push it in my context
    context.update(math.__dict__)

    # enable the greek letters for the corresponding constants
    context['π'] = math.pi
    context['τ'] = math.tau

    # all done
    return context


# declaration
class Numeric(Schema):
    """
    Intermediate class to mark the schemata that are numeric
    """

    # constants
    context = evaluationContext()


# end of file
