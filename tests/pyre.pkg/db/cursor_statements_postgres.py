#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statements postgres builds to declare a cursor over a selection, fetch its rows a few
at a time, and close it
"""


def test():
    """
    Ask the postgres mill for the three statements of a cursor, and check them
    """
    # access the package
    import pyre.db

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="cursors")
    # a selection, as the mill writes them
    selection = ("SELECT", "  name", "FROM granules;")
    # the statement that declares a cursor over it, which outlasts the transaction it is in
    assert tuple(mill.declareCursor(name="pyre_cursor_1", selection=selection)) == (
        "DECLARE pyre_cursor_1 NO SCROLL CURSOR WITH HOLD FOR",
        "  SELECT",
        "    name",
        "  FROM granules;",
    )
    # the one that fetches the next few of its rows
    assert tuple(mill.fetchFromCursor(name="pyre_cursor_1", count=1000)) == (
        "FETCH FORWARD 1000 FROM pyre_cursor_1;",
    )
    # and the one that closes it
    assert tuple(mill.closeCursor(name="pyre_cursor_1")) == ("CLOSE pyre_cursor_1;",)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
