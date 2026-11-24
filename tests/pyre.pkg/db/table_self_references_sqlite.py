#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite, which cannot add a reference to a table that exists, declares the references
of a table to itself when it makes the table, and adds none later
"""


def test():
    """
    Declare a table that refers to itself, and ask sqlite to make it without the reference
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the key
        label = pyre.db.int().primary()
        # and the granule it was derived from
        parent = pyre.db.int()

    # each granule may be derived from another
    Granule.pyre_foreignKey(field=Granule.parent, foreign=Granule.label, name="lineage")

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="table_self_references_sqlite")
    # build the statement that makes the table, without its references to itself
    statement = tuple(mill.createTable(table=Granule, selfReferences=False))
    # it declares the reference all the same
    assert any("CONSTRAINT lineage" in line for line in statement), statement
    # and there is nothing to add later
    assert tuple(mill.addSelfReferences(table=Granule)) == ()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
