#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statements standard SQL builds to set, release and roll back to a savepoint
"""


def test():
    """
    Ask the standard mill for the three statements of a savepoint, and check them
    """
    # access the package
    import pyre.db

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="savepoints")
    # the statement that sets a savepoint
    assert tuple(mill.savepoint(name="pyre_1")) == ("SAVEPOINT pyre_1;",)
    # the one that releases it
    assert tuple(mill.releaseSavepoint(name="pyre_1")) == ("RELEASE SAVEPOINT pyre_1;",)
    # and the one that undoes the work done since it was set
    assert tuple(mill.rollbackToSavepoint(name="pyre_1")) == ("ROLLBACK TO SAVEPOINT pyre_1;",)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
