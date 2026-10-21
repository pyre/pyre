#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The stream schemata accept the names of the process streams and open streams, and refuse every
other kind of value
"""


def test() -> None:
    """
    Give the stream schemata a value of each kind, and check what becomes of it
    """
    # externals
    import io
    import sys

    # support
    import pyre

    # make the stream schemata
    istream = pyre.schemata.istream()
    ostream = pyre.schemata.ostream()
    # an open stream in memory
    memory = io.StringIO()

    # the schema, the values, and what each one must become
    accepted = [
        # the names of the process streams
        (istream, "stdin", sys.stdin),
        (istream, "<stdin>", sys.stdin),
        (ostream, "stdout", sys.stdout),
        (ostream, "<stdout>", sys.stdout),
        (ostream, "stderr", sys.stderr),
        (ostream, "<stderr>", sys.stderr),
        # open streams
        (istream, memory, memory),
        (ostream, memory, memory),
        (ostream, sys.stdout, sys.stdout),
    ]
    # go through them
    for schema, value, expected in accepted:
        # coerce each one
        held = schema.coerce(value=value)
        # it must become the expected stream
        assert held is expected, f"{value!r}: {held!r}"

    # kinds the stream schemata do not support
    for schema in [istream, ostream]:
        # go through them
        for value in [0, 5, [], {}, {"k": "v"}]:
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
                assert False, f"{schema.typename} accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
