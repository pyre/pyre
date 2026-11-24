#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres keeps the rows without a match of a left join
"""


def test():
    """
    Store two granules, one with a product and one without, and select them with their kinds
    """
    # access the package
    import pyre.db

    # a table of products
    class Product(pyre.db.table, id="pyre_join_products"):
        """
        Products
        """

        # the key
        id = pyre.db.int()
        # and the kind
        kind = pyre.db.str()

    # a table of granules
    class Granule(pyre.db.table, id="pyre_join_granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str()
        # and the product it belongs to, if any
        product = pyre.db.int()

    # the granules, with the kinds of their products
    class Kinds(pyre.db.query, granule=Granule, product=Product):
        # the name of the granule
        name = granule.name
        # and the kind of its product
        kind = product.kind
        # matched on the product
        joins = pyre.db.leftJoin(product, on=granule.product == product.id)

    # connect
    db = pyre.db.postgres(name="join").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table of products
        db.createTable(Product)
        # and the table of granules
        db.createTable(Granule)
        # one product
        db.insert(Product.pyre_immutable(id=1, kind="RSLC"))
        # a granule that belongs to it, and one that belongs to none
        db.insert(
            Granule.pyre_immutable(name="a", product=1),
            Granule.pyre_immutable(name="b", product=None),
        )
        # select the granules with the kinds of their products
        rows = sorted((row.name, row.kind) for row in db.select(Kinds))
        # every granule is there, the one without a product without a kind
        assert rows == [("a", "RSLC"), ("b", None)], rows
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
