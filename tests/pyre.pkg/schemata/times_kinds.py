#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A time accepts the kinds it supports, converts the text it can parse, and refuses every other
kind of value, and text it cannot parse with the parser's reason
"""


def test() -> None:
    """
    Give a time a value of each kind, and check what becomes of it
    """
    # externals
    import datetime

    # support
    import pyre

    # make a time
    schema = pyre.schemata.time()

    # the values, and what each one must become
    accepted = [
        # a time
        (datetime.time(3, 4, 5), datetime.time(3, 4, 5)),
        # a timestamp, which loses its date
        (datetime.datetime(2020, 1, 2, 3, 4, 5), datetime.time(3, 4, 5)),
        # text, which may be padded
        (" 03:04:05 ", datetime.time(3, 4, 5)),
        # text with nothing in it
        ("", None),
        ("  ", None),
    ]
    # go through them
    for value, expected in accepted:
        # coerce each one
        held = schema.coerce(value=value)
        # it must become the expected value, of the expected type
        assert type(held) is type(expected) and held == expected, f"{value!r}: {held!r}"

    # kinds a time does not support, including those that are false
    for value in [0, 1.5, [], {}, {"k": "v"}]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # as a kind it does not support, so there is no reason beyond the complaint
            assert error.error is None, f"{value!r}: {error.error!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # carefully
    try:
        # coerce text the parser refuses
        schema.coerce(value="time")
    # it must be refused
    except schema.CastingError as error:
        # with the parser's reason
        assert isinstance(error.error, ValueError), repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted time"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
