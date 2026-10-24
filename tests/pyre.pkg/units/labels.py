#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that quantities spell out their units the way a person writes them, with the units in the
numerator first and those in the denominator after a slash, and that the text reads back as the
same quantity
"""


def test() -> None:
    """
    Spell out the units of quantities, and render the quantities as text
    """
    # support
    import pyre.units
    from pyre.units.SI import meter, second, kilogram, kelvin, ampere, mole, candela
    from pyre.units.SI import newton, hertz, joule, pascal

    # the units, and how they are spelled
    spellings = (
        (pyre.units.one, ""),
        (meter, "m"),
        (meter / second, "m/s"),
        (newton, "kg*m/s**2"),
        (hertz, "1/s"),
        (joule, "kg*m**2/s**2"),
        (pascal, "kg/(m*s**2)"),
        (kelvin / pascal, "m*s**2*K/kg"),
        (ampere * second / mole, "s*A/mol"),
        (1 / (meter * second), "1/(m*s)"),
        (meter**0.5, "m**0.5"),
        (candela / meter**2, "cd/m**2"),
        (kilogram * meter**-3, "kg/m**3"),
    )
    # go through them
    for units, spelling in spellings:
        # the units are spelled out
        assert units.label() == spelling, (spelling, units.label())

    # quantities, and their text
    renderings = (
        (2 * pyre.units.one, "2"),
        (2 * meter, "2.0*m"),
        (9.81 * newton, "9.81*kg*m/s**2"),
        (2 * hertz, "2.0/s"),
        (2 / (meter * second), "2.0/(m*s)"),
        (101325 * pascal, "101325.0*kg/(m*s**2)"),
    )
    # the parser, to read the text back
    parser = pyre.units.parser()
    # go through them
    for quantity, text in renderings:
        # the quantity renders as its text
        assert str(quantity) == text, (text, str(quantity))
        # which reads back as the same quantity
        assert parser.parse(text) == quantity, text

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
