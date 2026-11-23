#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the membership of a field in the rows of a query is written with IN over the
selection of the query
"""


def test():
    """
    Select the granules of the products of one kind, and check the statement
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
        # and the product it belongs to
        product = pyre.db.int()

    # the keys of the products of one kind
    class Wanted(pyre.db.query, product=Product):
        # the key
        id = product.id
        # of the products of the kind
        where = product.kind == "RSLC"

    # the granules of those products
    class Selected(pyre.db.query, granule=Granule):
        # the name of the granule
        name = granule.name
        # among the granules of the wanted products
        where = pyre.db.isIn(granule.product, Wanted)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="subqueries")
    # build the statement
    statement = tuple(mill.select(Selected))
    # and check it
    assert statement == (
        "SELECT",
        "    granule.name AS name",
        "  FROM",
        "    granules AS granule",
        "  WHERE",
        "    (granule.product IN (SELECT product.id AS id FROM products AS product"
        " WHERE ((product.kind) = ('RSLC'))));",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
