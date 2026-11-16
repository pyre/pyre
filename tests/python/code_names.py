#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The names compiled code uses, as variables or as attributes, are in its {co_names}, or in those
of the code objects among its constants, such as the bodies of lambdas; comprehensions put
theirs in one or the other, depending on the python; {pyre.calc.evaluation} walks them all to
refuse names that start with two underscores
"""

# externals
import types


def test() -> None:
    """
    Compile expressions and look for the names they use
    """
    # the expressions, and a name each one uses
    cases = [
        # a variable
        ("x + 1", "x"),
        # an attribute
        ("(1).real", "real"),
        # a chain of attributes
        ("().__class__.__base__", "__base__"),
        # an attribute in a comprehension
        ("[y.imag for y in [1]]", "imag"),
        # an attribute in the body of a lambda
        ("(lambda: (1).denominator)()", "denominator"),
    ]
    # go through them
    for text, name in cases:
        # compile each one
        program = compile(text, "<string>", "eval")
        # the name must be among those it uses
        assert name in set(names(program=program)), f"{text!r}: no {name!r}"

    # the body of a lambda
    program = compile("(lambda: (1).denominator)()", "<string>", "eval")
    # is a code object of its own, which the walk must visit
    assert "denominator" not in program.co_names, program.co_names

    # all done
    return


def names(*, program: types.CodeType):
    """
    Generate the names {program} uses, and those of the code among its constants
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


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
