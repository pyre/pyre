#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a stand-in for the catalog of an extension
class Stand:
    """
    A catalog that knows a few kinds by name and records what it is asked to make
    """

    # metamethods
    def __init__(self, products, factories):
        # the kinds of products i know
        self.products = dict(products)
        # and of factories
        self.factories = dict(factories)
        # what i was asked to make
        self.made = []
        # all done
        return

    # interface
    def makeProduct(self, decl, name, shape):
        """
        Record a request for a product
        """
        # remember it
        self.made.append(("product", decl, name, shape))
        # and answer with something recognizable
        return (self, decl)

    def makeFactory(self, decl, name):
        """
        Record a request for a factory
        """
        # remember it
        self.made.append(("factory", decl, name))
        # and answer with something recognizable
        return (self, decl)


def test():
    """
    Check that several catalogs are searched as one: their kinds are merged with the earlier ones
    winning, nodes are made by the catalog that knows their type, and the registry puts pyre's own
    catalog first, followed by the registered ones, each once
    """
    # support
    import pyre

    # two catalogs that share a kind of product
    first = Stand(products={"a": 1, "shared": 2}, factories={"f": 3, "g": 4})
    # and a kind of factory
    second = Stand(products={"b": 5, "shared": 6}, factories={"g": 7, "h": 8})
    # searched as one, the first one first
    catalogs = pyre.flow.recipes.federation(catalogs=[first, second])

    # the kinds of products are merged
    assert set(catalogs.products) == {"a", "b", "shared"}
    # and so are the kinds of factories
    assert set(catalogs.factories) == {"f", "g", "h"}
    # the first catalog answers for the products they share
    assert catalogs.products["shared"] == 2
    # and for the factories
    assert catalogs.factories["g"] == 4

    # a product is made by the catalog that knows its type
    assert catalogs.makeProduct(decl="b", name="p", shape=(2, 3)) == (second, "b")
    # a factory too
    assert catalogs.makeFactory(decl="h", name="q") == (second, "h")
    # and a shared one by the first
    assert catalogs.makeFactory(decl="g", name="r") == (first, "g")
    # so each catalog was asked for exactly what it makes: the first
    assert first.made == [("factory", "g", "r")]
    # and the second
    assert second.made == [("product", "b", "p", (2, 3)), ("factory", "h", "q")]
    # a product type nobody knows makes nothing
    assert catalogs.makeProduct(decl="nobody", name="s", shape=(1, 1)) is None
    # and neither does such a factory type
    assert catalogs.makeFactory(decl="nobody", name="t") is None

    # register the second catalog
    pyre.flow.recipes.register(catalog=second)
    # twice
    pyre.flow.recipes.register(catalog=second)
    # the catalogs recipes are staged against
    staged = pyre.flow.recipes.catalogs().catalogs
    # start with pyre's own
    assert staged[0] is pyre.libpyre.flow.catalog()
    # and include the registered one, once
    assert sum(catalog is second for catalog in staged) == 1

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
