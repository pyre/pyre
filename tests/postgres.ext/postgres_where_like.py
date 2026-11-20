#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a pattern with a quote in it matches what it says
"""


def test():
    """
    Select the streets whose name starts with O'Hara
    """
    # access the package
    import pyre.db

    # a table of streets
    class Street(pyre.db.table, id="pyre_where_like"):
        """
        Street names
        """

        # the name
        name = pyre.db.str()

    # the streets named after O'Hara
    class OHara(pyre.db.query, street=Street):
        """
        The streets named after O'Hara
        """

        # the field
        name = street.name
        # the restriction
        where = pyre.db.like(street.name, "O'Hara%")

    # connect
    db = pyre.db.postgres(name="queries").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Street)
        # with a few streets
        db.execute("INSERT INTO pyre_where_like (name) VALUES ('O''Hara Street'), ('Oak Street')")
        # only the one named after O'Hara qualifies
        found = [row.name for row in db.select(OHara)]
        # so check
        assert found == ["O'Hara Street"], found
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
