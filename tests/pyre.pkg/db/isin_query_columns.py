#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the membership of a field in a query of several columns is refused
"""


def test():
    """
    Test a field against a query of two columns, and check the mill refuses it
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

    # and the journal
    import journal

    # the refusal is expected, so its report goes nowhere
    journal.firewall("pyre.db").device = journal.trash()

    # the products of one kind, with two columns
    class Both(pyre.db.query, product=Product):
        # the key
        id = product.id
        # and the kind
        kind = product.kind

    # the granules of those products, which compare one value against rows of two
    class Wrong(pyre.db.query, granule=Granule):
        # the name of the granule
        name = granule.name
        # among the granules of the products
        where = pyre.db.isIn(granule.product, Both)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="subqueries")
    # attempt to
    try:
        # build the statement
        statement = tuple(mill.select(Wrong))
    # which must fail
    except journal.FirewallError as error:
        # whose report names the query
        assert "'Both'" in "\n".join(error.page), error.page
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
