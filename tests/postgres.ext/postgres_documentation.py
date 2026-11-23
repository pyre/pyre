#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres keeps the documentation of a table and its columns
"""


def test():
    """
    Create a documented table, and read its documentation from the catalog of the server
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="pyre_documentation"):
        """
        Daily readings, by city

        One row per city and day
        """

        # the city
        city = pyre.db.str(maxlen=32)
        city.doc = "the name of the city"
        # and the lowest reading
        low = pyre.db.float()

    # connect
    db = pyre.db.postgres(name="documentation").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Reading)
        # ask the catalog for the documentation of the table
        ((table, column),) = db.execute(
            "SELECT obj_description('pyre_documentation'::regclass, 'pg_class'),"
            " col_description('pyre_documentation'::regclass, 1)"
        )
        # the table keeps its whole docstring
        assert table == "Daily readings, by city\n\nOne row per city and day", repr(table)
        # and the column its documentation
        assert column == "the name of the city", repr(column)
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
