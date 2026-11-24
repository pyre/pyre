#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres names a violated check by the name it was declared with
"""


def test():
    """
    Violate a named check, and check the name the error carries
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of readings
    class Reading(pyre.db.table, id="pyre_constraint_named"):
        """
        Readings
        """

        # the lowest reading
        low = pyre.db.float()
        # and the highest
        high = pyre.db.float()

    # the lowest reading may not exceed the highest
    Reading.pyre_check(Reading.low <= Reading.high, name="ordered")

    # connect
    db = pyre.db.postgres(name="constraint_named").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Reading)
        # attempt to
        try:
            # insert a reading whose low exceeds its high
            db.insert(Reading.pyre_immutable(low=2.0, high=1.0))
        # which must fail
        except exceptions.IntegrityError as error:
            # naming the check
            assert error.constraint == "ordered", error.constraint
        # if it doesn't
        else:
            # the check was not applied
            assert False, "a reading whose low exceeds its high was accepted"
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
