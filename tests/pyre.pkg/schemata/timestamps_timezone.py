#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A timestamp that says whether its values carry a time zone refuses the moments that disagree
"""


def test() -> None:
    """
    Give timestamps that insist on a zone, or on none, the moments they must refuse
    """
    # support
    import datetime
    import pyre

    # a moment with a zone
    aware = datetime.datetime(2026, 11, 19, 3, 4, 5, tzinfo=datetime.timezone.utc)
    # and one without
    naive = datetime.datetime(2026, 11, 19, 3, 4, 5)

    # a timestamp that accepts either
    either = pyre.schemata.timestamp()
    # takes the moment with a zone
    assert either.coerce(value=aware) == aware
    # and the one without
    assert either.coerce(value=naive) == naive

    # each kind of timestamp, and the moments it must refuse, as values and as text
    cases = [
        (pyre.schemata.timestamp(timezone=True), [naive, "2026-11-19 03:04:05"]),
        (pyre.schemata.timestamp(timezone=False), [aware, "2026-11-19 03:04:05+00:00"]),
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
