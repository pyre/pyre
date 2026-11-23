#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres creates a database that exists already without complaint, when asked
to
"""


def test():
    """
    Create a database twice, the second time allowing it to exist
    """
    # access the package
    import pyre.db

    # connect
    db = pyre.db.postgres(name="database_exist_ok").attach()
    # carefully
    try:
        # make the database
        db.createDatabase(name="pyre_exist_ok")
        # and again, allowing it to exist
        db.createDatabase(name="pyre_exist_ok", existOk=True)
    # either way
    finally:
        # leave nothing behind
        db.execute("DROP DATABASE IF EXISTS pyre_exist_ok")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
