#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres drops a database that is not there without complaint, when asked to
"""


def test():
    """
    Drop a database that was never made, allowing it to be missing
    """
    # access the package
    import pyre.db

    # connect
    db = pyre.db.postgres(name="database_missing_ok").attach()
    # drop a database that was never made, allowing it to be missing
    db.dropDatabase(name="pyre_missing_ok", missingOk=True)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
