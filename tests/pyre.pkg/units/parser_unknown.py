#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser of quantities reports the names it does not know, such as misspelled units,
and that the report is still a {NameError}
"""


def test() -> None:
    """
    Parse quantities with names the parser does not know
    """
    # support
    import pyre.units
    from pyre.units.exceptions import UnknownUnitError

    # the parser
    parser = pyre.units.parser()
    # text, and the name in it the parser does not know
    for text, name in (
        ("2*furlongs", "furlongs"),
        ("3*metr", "metr"),
        ("sqroot(2)*meter", "sqroot"),
    ):
        # attempt to
        try:
            # parse it
            parser.parse(text)
            # which should be unreachable
            assert False, text
        # if it is refused, as expected
        except UnknownUnitError as error:
            # the report names what the parser does not know
            assert error.name == name, (text, error.name)
            # says so
            assert str(error) == f"{name!r} is not a unit", str(error)
            # and is still a {NameError}, for those that catch one
            assert isinstance(error, NameError), type(error)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
