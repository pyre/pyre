#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dimensional refuses text with a name the parser does not know, such as a misspelled
unit, and says which one
"""


def test() -> None:
    """
    Coerce text with unknown names into a dimensional
    """
    # support
    import pyre.schemata
    from pyre.units.exceptions import UnknownUnitError

    # make a schema
    schema = pyre.schemata.dimensional()
    # text, and the name in it the parser does not know
    for text, name in (("2*furlongs", "furlongs"), ("3*metr", "metr")):
        # attempt to
        try:
            # coerce it
            schema.coerce(value=text)
            # which should be unreachable
            assert False, text
        # if it is refused, as expected
        except schema.CastingError as error:
            # because of the unknown name
            assert isinstance(error.error, UnknownUnitError), repr(error.error)
            # which the complaint names
            assert str(error) == (
                f"could not coerce {text!r} into a dimensional quantity: {name!r} is not a unit"
            ), str(error)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
