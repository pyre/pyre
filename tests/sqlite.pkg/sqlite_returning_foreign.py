#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the fields an insert returns must belong to the table of its records
"""


def test():
    """
    Insert a granule, asking for a field of another table, and check the server refuses it
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # and the journal
    import journal

    # another table
    class Product(pyre.db.table, id="products"):
        # the key
        id = pyre.db.int().primary()

    # connect to a database in memory
    db = pyre.db.sqlite(name="returning").attach()
    # make the table of granules
    db.createTable(Granule)
    # attempt to
    try:
        # insert a granule, asking for the key of a product
        db.insert(Granule.pyre_immutable(id=1, name="first"), returning=Product.id)
    # which must fail
    except journal.FirewallError as error:
        # whose report names the two tables
        report = "\n".join(error.page)
        # the one of the records
        assert "'granules'" in report, report
        # and the one of the fields
        assert "'products'" in report, report
    # if it doesn't
    else:
        # the insert went through anyway
        assert False, "the insert returned fields of another table"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
