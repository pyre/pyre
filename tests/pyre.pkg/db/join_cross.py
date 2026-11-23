#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the tables of a query that are not joined are crossed when others are joined
"""


def test():
    """
    Join the products to the granules of a query with a third table, and check the statement
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

    # a table of orbits
    class Orbit(pyre.db.table, id="orbits"):
        # the number
        number = pyre.db.int()

    # the granules, with the kinds of their products
    class Kinds(pyre.db.query, granule=Granule, orbit=Orbit, product=Product):
        # the name of the granule
        name = granule.name
        # and the kind of its product
        kind = product.kind
        # and the number of the orbit
        number = orbit.number
        # matched on the product
        joins = pyre.db.join(product, on=granule.product == product.id)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="joins")
    # build the statement
    statement = tuple(mill.select(Kinds))
    # and check it
    assert statement == (
        "SELECT",
        "    granule.name AS name,",
        "    product.kind AS kind,",
        "    orbit.number AS number",
        "  FROM",
        "    granules AS granule",
        "    CROSS JOIN orbits AS orbit",
        "    JOIN products AS product ON ((granule.product) = (product.id));",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
