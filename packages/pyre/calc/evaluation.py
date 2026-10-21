# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import builtins
import types

# the local exceptions
from .exceptions import DisallowedFunctionError, DisallowedNameError

# the builtins the value of a setting may use, in groups that the refusals list a line each
functions = {
    "numbers": (bool, complex, float, int),
    "arithmetic": (abs, divmod, max, min, pow, round, sum),
    "text": (len, str),
}
# indexed by name, the way the interpreter looks them up
allowed = {function.__name__: function for group in functions.values() for function in group}
# the ways an evaluation can fail, now that the builtins and the names it may use are closed;
# {tests/pyre.pkg/calc/evaluation_exceptions.py} fails when a python adds builtin exceptions
# that are neither here nor excluded there for a reason
errors = (
    SyntaxError,
    NameError,
    AttributeError,
    LookupError,
    TypeError,
    ValueError,
    ArithmeticError,
    RecursionError,
)
# the names of all the builtin functions, so a refusal can say which ones are allowed
builtinFunctions = {
    name for name, value in vars(builtins).items() if isinstance(value, types.BuiltinFunctionType)
}


# the evaluator
def evaluate(*, expression: str | types.CodeType, context: dict) -> object:
    """
    Evaluate {expression} in {context}, with access to the {allowed} builtins and no others
    """
    # start with {expression} itself
    program = expression
    # if it is text
    if isinstance(expression, str):
        # compile it, so its names can be checked before any of it runs; leading spaces and
        # tabs are dropped, as the interpreter does when it evaluates text, which
        # {tests/python/eval_whitespace.py} checks
        program = compile(expression.lstrip(" \t"), "<string>", "eval")
    # go through the names it uses, as variables or attributes
    for name in names(program=program):
        # the ordinary ones
        if not name.startswith("__"):
            # are fine
            continue
        # a builtin function with such a name
        if name in builtinFunctions:
            # is refused like the other builtins a setting may not use
            raise DisallowedFunctionError(name=name)
        # and any other reaches past the builtins, so refuse it
        raise DisallowedNameError(name=name)
    # give the evaluation the allowed builtins; the interpreter would have added all of them
    # to {context} on its own, which {tests/python/eval_builtins.py} checks
    context["__builtins__"] = allowed
    # attempt to
    try:
        # evaluate the program
        value = eval(program, context)
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


def names(*, program: types.CodeType):
    """
    Generate the names {program} uses as variables or attributes, including those used by the
    code it holds, such as the bodies of lambdas; {tests/python/code_names.py} checks where the
    interpreter puts them
    """
    # the names of the program itself
    yield from program.co_names
    # go through its constants
    for constant in program.co_consts:
        # the ones that are code
        if isinstance(constant, types.CodeType):
            # contribute their names
            yield from names(program=constant)
    # all done
    return


# end of file
