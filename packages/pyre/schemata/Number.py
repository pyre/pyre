# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import math

# the evaluator of text
from ..calc.evaluation import evaluate, errors
from ..calc.exceptions import DisallowedNameError

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

    # interface
    def evaluate(self, *, value: str) -> object:
        """
        Evaluate the text in {value} in my context, with access to the builtins that the value
        of a setting may use
        """
        # attempt to
        try:
            # get the interpreter to evaluate simple expressions
            candidate = evaluate(expression=value, context=self.context)
        # if it uses a function or a name the value of a setting may not
        except DisallowedNameError as error:
            # say so, in words the user can act on
            raise self.CastingError(value=value, description=str(error), error=error)
        # if it fails in any of the ways an evaluation can
        except errors as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # if all goes well, return the {candidate}
        return candidate

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
