#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite selects the rows whose field is among the rows of a query
"""


def test():
    """
    Store two products and their granules, and select the granules of one kind of product
    """
    # access the package
    import pyre.db

    # a table of products
    class Product(pyre.db.table, id="products"):
        """
        Products
        """

        # the key
        id = pyre.db.int()
        # and the kind
        kind = pyre.db.str()

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

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

    # connect
    db = pyre.db.sqlite(name="isin_query").attach()
    # make the table of products
    db.createTable(Product)
    # and the table of granules
    db.createTable(Granule)
    # two products of different kinds
    db.insert(
        Product.pyre_immutable(id=1, kind="RSLC"),
        Product.pyre_immutable(id=2, kind="GCOV"),
    )
    # and a granule of each
    db.insert(
        Granule.pyre_immutable(name="a", product=1),
        Granule.pyre_immutable(name="b", product=2),
    )
    # select the granules of the wanted products
    names = [row.name for row in db.select(Selected)]
    # which is the granule of the product of the wanted kind
    assert names == ["a"], names
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
