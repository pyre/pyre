#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A string lets an error raised by the value's own conversion to text through as itself, rather
than reporting a defect in the value's class as a value it refuses
"""


def test() -> None:
    """
    Give a string a value whose conversion to text fails, and check the error gets through
    """
    # support
    import pyre

    # the error the conversion raises
    class Broken(Exception):
        """
        The defect in the value's class
        """

    # a value whose conversion to text fails
    class Value:
        """
        A value with a defective conversion to text
        """

        # the conversion
        def __str__(self) -> str:
            """
            Fail
            """
            # by raising the defect
            raise Broken()

    # make a string
    schema = pyre.schemata.str()
    # carefully
    try:
        # coerce the value
        schema.coerce(value=Value())
    # the defect must get through
    except Broken:
        # as itself
        pass
    # if it is reported as a refusal instead
    except schema.CastingError as error:
        # say so
        assert False, f"refused, with reason {error.error!r}"
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted a value that cannot be text"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
