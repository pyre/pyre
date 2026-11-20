#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A time that says whether its values carry a time zone refuses the times that disagree
"""


def test() -> None:
    """
    Give times that insist on a zone, or on none, the values they must refuse
    """
    # support
    import datetime
    import pyre

    # a time with a zone
    aware = datetime.time(3, 4, 5, tzinfo=datetime.timezone.utc)
    # and one without
    naive = datetime.time(3, 4, 5)

    # each kind of time, and the values it must refuse, as values and as text
    cases = [
        (pyre.schemata.time(timezone=True), [naive, "03:04:05"]),
        (pyre.schemata.time(timezone=False), [aware, "03:04:05+00:00"]),
    ]
    # go through them
    for schema, refusals in cases:
        # and each value
        for value in refusals:
            # carefully
            try:
                # coerce it
                schema.coerce(value=value)
            # it must be refused
            except schema.CastingError:
                # which is the whole point
                pass
            # if it is not refused at all
            else:
                # say so
                assert False, f"timezone={schema.timezone} accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
