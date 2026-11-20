#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a session spells its values the way the bindings read them, whatever the caller
asked for when it connected
"""


def test():
    """
    Ask for a different date style and encoding, and check what the session uses
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session that asks for other settings
    connection = libpq.Connection(
        {"dbname": "postgres", "options": "-c DateStyle=SQL,DMY", "client_encoding": "LATIN1"}
    )
    # ask what it uses
    row = connection.exec(
        "SELECT current_setting('DateStyle') AS style,"
        " current_setting('client_encoding') AS encoding"
    )[0]
    # dates are written the ISO way
    assert row["style"].startswith("ISO"), repr(row["style"])
    # and text is utf-8
    assert row["encoding"] == "UTF8", repr(row["encoding"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
