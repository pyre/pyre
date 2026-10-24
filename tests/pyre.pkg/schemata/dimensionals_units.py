#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dimensional with units accepts the values that have them, refuses those that do not,
and says which units it expected and which it got
"""


def test() -> None:
    """
    Coerce values into dimensionals with units
    """
    # support
    import pyre.schemata
    from pyre.units import one
    from pyre.units.SI import meter, second, newton
    from pyre.units.length import km

    # a length accepts other units of length
    assert pyre.schemata.dimensional(units=meter).coerce(value="2*km") == 2 * km
    # a quantity given directly
    assert pyre.schemata.dimensional(units=meter).coerce(value=2 * km) == 2 * km
    # and the result of an expression
    assert pyre.schemata.dimensional(units=meter).coerce(value="(1+1)*meter/second*second")
    # a quantity without units accepts numbers
    assert pyre.schemata.dimensional(units=one).coerce(value="2") == 2
    # and quantities whose units cancel
    assert pyre.schemata.dimensional(units=one).coerce(value="2*meter/meter") == 2
    # without units, anything goes
    assert pyre.schemata.dimensional().coerce(value="2*second") == 2 * second

    # the units, what they measure, the value, and the complaint
    refusals = (
        (
            newton,
            "force",
            "5*kilogram*meter/second",
            "could not convert '5*kilogram*meter/second' to units of 'force' (kg*m/s**2):"
            " it is in kg*m/s",
        ),
        (
            meter / second,
            "speed",
            "3",
            "could not convert '3' to units of 'speed' (m/s): it has no units",
        ),
        (
            one,
            "strain",
            "2*meter",
            "could not convert '2*meter' to units of 'strain' (none): it is in m",
        ),
        (
            newton,
            None,
            "2*second",
            "could not convert '2*second' to units of kg*m/s**2: it is in s",
        ),
        (
            one,
            None,
            "2*meter",
            "could not convert '2*meter' to a quantity without units: it is in m",
        ),
        (
            meter / second,
            None,
            3,
            "could not convert 3 to units of m/s: it has no units",
        ),
    )
    # go through them
    for units, quantity, value, complaint in refusals:
        # make a schema
        schema = pyre.schemata.dimensional(units=units, quantity=quantity)
        # attempt to
        try:
            # coerce the value
            schema.coerce(value=value)
            # which should be unreachable
            assert False, value
        # if it is refused, as expected
        except schema.CastingError as error:
            # with the complaint
            assert str(error) == complaint, str(error)
            # which keeps what the schema measures
            assert error.quantity == quantity, error.quantity

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
