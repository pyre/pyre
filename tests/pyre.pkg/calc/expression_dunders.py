#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An expression may not use names that start with two underscores, as variables or attributes,
since they reach past the builtins a setting is allowed; other attributes are fine
"""


def test() -> None:
    """
    Evaluate expressions that use such names, and some that use ordinary attributes
    """
    # support
    import pyre.calc
    from pyre.calc.exceptions import DisallowedFunctionError, DisallowedNameError

    # a model
    model = pyre.calc.model()
    # with a node to refer to
    model["a"] = 2

    # expressions that use ordinary attributes, and their values
    allowed = [
        ("{a}.real", 2),
        ("complex({a}, 1).imag", 1.0),
        ("str({a}).zfill(3)", "002"),
        ("[x * x for x in [{a}]]", [4]),
    ]
    # go through them
    for formula, expected in allowed:
        # make an expression
        model["x"] = model.expression(formula)
        # its value must be the expected one
        assert model["x"] == expected, f"{formula!r}: {model['x']!r}"

    # the text of the refusal of {__class__}
    report = (
        "'__class__' can't be used in the value of a setting; "
        "names that start with two underscores are off limits"
    )
    # expressions that use such names, and the name each one is refused for
    disallowed = [
        ("().__class__.__base__.__subclasses__() and {a}", "__class__"),
        ("{a}.__class__", "__class__"),
        ("__builtins__ and {a}", "__builtins__"),
        ("[x.__doc__ for x in [{a}]]", "__doc__"),
        ("(lambda: {a}.__dict__)()", "__dict__"),
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
            # because of the name
            assert type(error.error) is DisallowedNameError, f"{formula!r}: {error.error!r}"
            # which it names
            assert error.error.name == name, f"{formula!r}: {error.error.name!r}"
            # and the text of the refusal of {__class__}
            if name == "__class__":
                # must be the one users see
                assert str(error.error) == report, str(error.error)
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {formula!r}"

    # a builtin with such a name
    model["x"] = model.expression("__import__('os') and {a}")
    # carefully
    try:
        # read its value
        model["x"]
    # it must be refused
    except model.EvaluationError as error:
        # as a builtin a setting may not use, which says which ones it may
        assert isinstance(error.error, DisallowedFunctionError), repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted __import__"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
