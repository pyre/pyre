#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An expression that fails is refused with an evaluation error about it that carries the reason;
an expression that refers to another that fails lets the refusal of the other one through, so
it names the expression that is actually wrong
"""


def test() -> None:
    """
    Evaluate expressions that fail in each of the ways an evaluation can, and one that refers
    to an expression that fails
    """
    # support
    import pyre.calc

    # a model
    model = pyre.calc.model()
    # with a node to refer to
    model["a"] = 2

    # expressions that fail, and the kind of their reason
    failures = [
        ("{a} / 0", ZeroDivisionError),
        ("10.0 ** (400 * {a})", OverflowError),
        ("{a}.nothing", AttributeError),
        ("[{a}][5]", IndexError),
        ("{{}}['k'] or {a}", KeyError),
        ("'text' + {a}", TypeError),
        ("int('text') + {a}", ValueError),
        ("nothing + {a}", NameError),
        ("(lambda f: f(f))(lambda f: f(f)) + {a}", RecursionError),
    ]
    # go through them
    for formula, reason in failures:
        # make an expression
        model["x"] = model.expression(formula)
        # carefully
        try:
            # read its value
            model["x"]
        # it must be refused
        except model.EvaluationError as error:
            # with the reason
            assert isinstance(error.error, reason), f"{formula!r}: {error.error!r}"
            # by the expression itself
            assert error.node is model.retrieve(name="x"), f"{formula!r}: {error.node}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {formula!r}"

    # an expression that fails
    model["inner"] = model.expression("{a} / 0")
    # and one that refers to it
    model["outer"] = model.expression("{inner} + 1")
    # carefully
    try:
        # read the value of the one that refers to the other
        model["outer"]
    # it must be refused
    except model.EvaluationError as error:
        # by the expression that fails
        assert error.node is model.retrieve(name="inner"), error.node
        # with its reason
        assert isinstance(error.error, ZeroDivisionError), repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted an expression that refers to one that fails"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
