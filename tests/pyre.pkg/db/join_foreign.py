#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a join of a table the query does not name is refused
"""


def test():
    """
    Join a table that is not among the tables of the query, and check the mill refuses it
    """
    # access the package
    import pyre.db

    # a table of products
    class Product(pyre.db.table, id="products"):
        # the key
        id = pyre.db.int()
        # and the kind
        kind = pyre.db.str()

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the name
        name = pyre.db.str()
        # and the product it belongs to, if any
        product = pyre.db.int()

    # and the journal
    import journal

    # the granules, with a join of a table the query does not name
    class Kinds(pyre.db.query, granule=Granule):
        # the name of the granule
        name = granule.name
        # matched on a product it does not know
        joins = pyre.db.join(Product, on=granule.product == Product.id)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="joins")
    # attempt to
    try:
        # build the statement
        statement = tuple(mill.select(Kinds))
    # which must fail
    except journal.FirewallError as error:
        # whose report names the table
        assert "'products'" in "\n".join(error.page), error.page
    # if it doesn't
    else:
        # the statement was built anyway
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
