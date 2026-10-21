#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Text that a numeric or dimensional setting fails to evaluate is refused with the reason, in
each of the ways an evaluation can fail
"""


def test() -> None:
    """
    Give numeric and dimensional schemata text that fails to evaluate
    """
    # support
    import pyre
    from pyre.units.exceptions import CompatibilityError

    # text that fails, and the kind of its reason
    failures = [
        ("1 +", SyntaxError),
        ("1\n2", SyntaxError),
        ("nothing", NameError),
        ("(1).nothing", AttributeError),
        ("[1][5]", IndexError),
        ("{}['k']", KeyError),
        ("'text' + 1", TypeError),
        ("int('text')", ValueError),
        ("1 / 0", ZeroDivisionError),
        ("10.0 ** 400", OverflowError),
        ("(lambda f: f(f))(lambda f: f(f))", RecursionError),
    ]
    # the numeric schemata
    for schema in [pyre.schemata.int(), pyre.schemata.float(), pyre.schemata.complex()]:
        # go through the failures
        for text, reason in failures:
            # carefully
            try:
                # coerce each one
                schema.coerce(value=text)
            # it must be refused
            except schema.CastingError as error:
                # with the reason
                assert isinstance(error.error, reason), f"{schema}, {text!r}: {error.error!r}"
            # if it is not refused at all
            else:
                # say so
                assert False, f"{schema} accepted {text!r}"

    # a dimensional
    schema = pyre.schemata.dimensional()
    # the values it fails to evaluate, and the kind of their reason
    failures = [
        ("meter + second", CompatibilityError),
        ("meter + 1", TypeError),
        ("meter.nothing", AttributeError),
        ("meter / 0", ZeroDivisionError),
        ("meter +", SyntaxError),
        (5, AttributeError),
    ]
    # go through them
    for value, reason in failures:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # with the reason
            assert isinstance(error.error, reason), f"{value!r}: {error.error!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
