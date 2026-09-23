#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a failed coercion carries the reason the converter gave, and that the report of
the error passes it along after the framework's own description
"""

# support
import pyre


def test():
    # go through the processors, with a value each one refuses
    for schema, value in (
        (pyre.schemata.timestamp(), "1992-13-45 25:61:00"),
        (pyre.schemata.date(), "1992-13-45"),
        (pyre.schemata.time(), "25:61:00"),
        (pyre.schemata.int(), "not-a-number"),
        (pyre.schemata.float(), "not-a-number"),
        (pyre.schemata.decimal(), "not-a-number"),
        (pyre.schemata.complex(), "not-a-number"),
        (pyre.schemata.fraction(), "not-a-number"),
    ):
        # attempt to
        try:
            # coerce a value the parser refuses
            schema.coerce(value=value)
            # which must fail
            assert False, "unreachable"
        # and when it does
        except schema.CastingError as error:
            # the one line description names the value
            assert repr(value) in str(error)
            # the converter's reason rides along
            assert isinstance(error.error, Exception)
            # and the report has it, after the description
            report = list(error._pyre_report())
            assert report[0] == str(error)
            assert report[-1] == f"reason: {error.error}"
    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
