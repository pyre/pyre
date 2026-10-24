#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The text of a numeric, dimensional or array setting may use only the builtins a setting is
allowed: the others are refused with a complaint that names the function and lists the ones
allowed; so are names that start with two underscores; a name that is not a builtin at all is
refused as an unknown name
"""


def test() -> None:
    """
    Give each schema that evaluates text a value that uses an allowed builtin, a disallowed one,
    and an unknown name
    """
    # support
    import pyre
    from pyre.calc.exceptions import DisallowedFunctionError, DisallowedNameError

    # get the units
    meter = pyre.units.SI.meter

    # the schemata, with text that uses allowed builtins and what it must become
    allowed = [
        (pyre.schemata.int(), "abs(-2)", 2),
        (pyre.schemata.int(), "len(str(10))", 2),
        (pyre.schemata.float(), "max(1, 2.5)", 2.5),
        (pyre.schemata.complex(), "complex(1, 2)", 1 + 2j),
        (pyre.schemata.dimensional(), "abs(-2)*meter", 2 * meter),
        (pyre.schemata.array(), "[abs(-1), 2]", (1.0, 2.0)),
    ]
    # go through them
    for schema, text, expected in allowed:
        # coerce each one
        held = schema.coerce(value=text)
        # it must become the expected value
        assert held == expected, f"{text!r}: {held!r}"

    # the first line of the refusal of {open}
    first = "'open' can't be used in the value of a setting; the functions allowed are"
    # the schemata that refuse text that uses a builtin a setting may not
    for schema in [
        pyre.schemata.int(),
        pyre.schemata.float(),
        pyre.schemata.complex(),
        pyre.schemata.dimensional(),
    ]:
        # carefully
        try:
            # coerce text that opens a file
            schema.coerce(value="open('/dev/null')")
        # it must be refused
        except schema.CastingError as error:
            # because of the builtin
            assert isinstance(error.error, DisallowedFunctionError), repr(error.error)
            # with a complaint that says so, so users see it
            assert str(error).startswith(first), str(error)
        # if it is not refused at all
        else:
            # say so
            assert False, f"{schema} accepted open"

    # the first line of the refusal of {__class__}
    first = "'__class__' can't be used in the value of a setting"
    # the schemata that refuse text that reaches past the builtins through such names
    for schema in [
        pyre.schemata.int(),
        pyre.schemata.float(),
        pyre.schemata.complex(),
        pyre.schemata.dimensional(),
    ]:
        # carefully
        try:
            # coerce text that walks up the class hierarchy
            schema.coerce(value="(1).__class__")
        # it must be refused
        except schema.CastingError as error:
            # because of the name
            assert isinstance(error.error, DisallowedNameError), repr(error.error)
            # with a complaint that says so, so users see it
            assert str(error).startswith(first), str(error)
        # if it is not refused at all
        else:
            # say so
            assert False, f"{schema} accepted __class__"

    # an array
    schema = pyre.schemata.array()
    # carefully
    try:
        # coerce text that imports a module
        schema.coerce(value="[__import__('os').getpid()]")
    # it must be refused, the way numbers refuse it
    except schema.CastingError as error:
        # because of the builtin it names
        assert isinstance(error.error, DisallowedFunctionError), repr(error.error)
        # which the complaint keeps
        assert error.error.name == "__import__", error.error.name
    # if it is not refused at all
    else:
        # say so
        assert False, "the array accepted __import__"

    # the schemata that refuse text that uses an unknown name
    for schema in [pyre.schemata.int(), pyre.schemata.float(), pyre.schemata.complex()]:
        # carefully
        try:
            # coerce text with a name that is not defined
            schema.coerce(value="nothing")
        # it must be refused
        except schema.CastingError as error:
            # as an unknown name
            assert type(error.error) is NameError, repr(error.error)
        # if it is not refused at all
        else:
            # say so
            assert False, f"{schema} accepted an unknown name"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
