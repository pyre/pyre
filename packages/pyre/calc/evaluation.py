# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import builtins
import types

# the local exceptions
from .exceptions import DisallowedFunctionError

# the builtins the value of a setting may use, in groups that the refusals list a line each
functions = {
    "numbers": (bool, complex, float, int),
    "arithmetic": (abs, divmod, max, min, pow, round, sum),
    "text": (len, str),
}
# indexed by name, the way the interpreter looks them up
allowed = {function.__name__: function for group in functions.values() for function in group}


# the evaluator
def evaluate(*, expression: str | types.CodeType, context: dict) -> object:
    """
    Evaluate {expression} in {context}, with access to the {allowed} builtins and no others
    """
    # give the evaluation the allowed builtins; the interpreter would have added all of them
    # to {context} on its own
    context["__builtins__"] = allowed
    # attempt to
    try:
        # evaluate the expression
        value = eval(expression, context)
    # if it refers to a name that is not defined
    except NameError as error:
        # and the name belongs to a builtin that is not allowed
        if error.name in vars(builtins):
            # say so, in words the user can act on
            raise DisallowedFunctionError(name=error.name) from error
        # otherwise, the name is simply unknown, which is not mine to explain
        raise
    # if all goes well, return the {value}
    return value


# end of file
