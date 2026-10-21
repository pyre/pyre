#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An expression may use only the builtins a setting is allowed: the others are refused with an
error that names the function and lists the ones allowed; a name that is not a builtin at all
is still just an unknown name
"""


def test() -> None:
    """
    Evaluate expressions that use allowed builtins, disallowed ones, and unknown names
    """
    # support
    import pyre.calc
    from pyre.calc.exceptions import DisallowedFunctionError

    # a model
    model = pyre.calc.model()
    # with a node to refer to
    model["a"] = -2

    # expressions that use the allowed builtins, and their values
    allowed = [
        ("abs({a})", 2),
        ("max({a}, 3)", 3),
        ("min({a}, 3)", -2),
        ("round({a} / 3)", -1),
        ("pow({a}, 2)", 4),
        ("sum([{a}, 1])", -1),
        ("divmod({a}, 3)", (-1, 1)),
        ("int({a} / 2)", -1),
        ("float({a})", -2.0),
        ("complex({a}, 1)", -2 + 1j),
        ("bool({a})", True),
        ("len(str({a}))", 2),
    ]
    # go through them
    for formula, expected in allowed:
        # make an expression
        model["x"] = model.expression(formula)
        # its value must be the expected one
        assert model["x"] == expected, f"{formula!r}: {model['x']!r}"

    # the text of the refusal of {open}
    report = "\n".join(
        [
            "'open' can't be used in the value of a setting; the functions allowed are",
            "  numbers: bool, complex, float, int",
            "  arithmetic: abs, divmod, max, min, pow, round, sum",
            "  text: len, str",
        ]
    )
    # expressions that use builtins a setting may not, and the builtin each one names
    disallowed = [
        ("open({a})", "open"),
        ("__import__('os') and {a}", "__import__"),
        ("exec('1') or {a}", "exec"),
        ("eval('1') + {a}", "eval"),
    ]
    # go through them
    for formula, name in disallowed:
        # make an expression
        model["x"] = model.expression(formula)
        # carefully
        try:
            # read its value
            model["x"]
        # it must be refused
        except model.EvaluationError as error:
            # because of the builtin
            assert isinstance(error.error, DisallowedFunctionError), f"{formula!r}: {error!r}"
            # which it names
            assert error.error.name == name, f"{formula!r}: {error.error.name!r}"
            # and the text of the refusal of {open}
            if name == "open":
                # must be the one users see
                assert str(error.error) == report, str(error.error)
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {formula!r}"

    # an expression that uses a name that is not a builtin
    model["x"] = model.expression("nothing + {a}")
    # carefully
    try:
        # read its value
        model["x"]
    # it must be refused
    except model.EvaluationError as error:
        # as an unknown name
        assert type(error.error) is NameError, repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted an unknown name"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
