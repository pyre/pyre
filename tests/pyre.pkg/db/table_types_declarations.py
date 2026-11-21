#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the SQL types the columns declare: times of day and moments, with or without their time
zones, strings of octets, identifiers, and arrays of the types of their entries
"""


def test():
    """
    Declare a column of each type, and check what it declares
    """
    # access the package
    import pyre.db

    # each column, and the type it must declare
    columns = [
        # dates
        (pyre.db.date(), "DATE"),
        # times of day, without their offsets
        (pyre.db.time(), "TIME"),
        # and with them
        (pyre.db.time(timezone=True), "TIME WITH TIME ZONE"),
        # moments, without their time zones
        (pyre.db.timestamp(), "TIMESTAMP"),
        # and with them
        (pyre.db.timestamp(timezone=True), "TIMESTAMP WITH TIME ZONE"),
        # strings of octets
        (pyre.db.bytes(), "BYTEA"),
        # identifiers
        (pyre.db.uuid(), "UUID"),
        # arrays of integers
        (pyre.db.array(schema=pyre.db.int()), "INTEGER[]"),
        # whatever their rank
        (pyre.db.array(schema=pyre.db.int(), rank=2), "INTEGER[]"),
        # and arrays of strings
        (pyre.db.array(schema=pyre.db.str()), "TEXT[]"),
    ]
    # go through them
    for column, decl in columns:
        # each one declares its type
        assert column.decl == decl, (column.decl, decl)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
