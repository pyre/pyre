# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the catalogs of several extensions, searched as one
class Catalogs:
    """
    The catalogs of the extensions that compiled flow nodes in, searched in order as if they
    were one: each extension keeps the catalog of the instantiations it was compiled with, and
    a recipe is staged against all of them, so a graph can mix the nodes of several extensions
    """

    # interface
    @property
    def products(self) -> dict:
        """
        The kinds of products my catalogs know, by the declarations of their types; a kind
        known to more than one is answered for by the first
        """
        # the merged table
        products = {}
        # go through my catalogs, last to first, so the earlier ones win
        for catalog in reversed(self.catalogs):
            # fold in what this one knows
            products.update(catalog.products)
        # hand it off
        return products

    @property
    def factories(self) -> dict:
        """
        The kinds of factories my catalogs know, by the declarations of their types; a kind
        known to more than one is answered for by the first
        """
        # the merged table
        factories = {}
        # go through my catalogs, last to first, so the earlier ones win
        for catalog in reversed(self.catalogs):
            # fold in what this one knows
            factories.update(catalog.factories)
        # hand it off
        return factories

    def makeProduct(self, *, decl: str, name: str, shape: tuple):
        """
        Make a product of the type declared as {decl}, called {name}, of the given {shape}, by
        asking the first of my catalogs that knows the type; nothing when none does, or when
        the one that does cannot make it from a shape
        """
        # find the catalog that knows the type
        catalog = self.owner(decl=decl, table="products")
        # if there is none
        if catalog is None:
            # there is nothing to make
            return None
        # otherwise, ask it
        return catalog.makeProduct(decl=decl, name=name, shape=shape)

    def makeFactory(self, *, decl: str, name: str):
        """
        Make a factory of the type declared as {decl}, called {name}, by asking the first of my
        catalogs that knows the type; nothing when none does
        """
        # find the catalog that knows the type
        catalog = self.owner(decl=decl, table="factories")
        # if there is none
        if catalog is None:
            # there is nothing to make
            return None
        # otherwise, ask it
        return catalog.makeFactory(decl=decl, name=name)

    def owner(self, *, decl: str, table: str):
        """
        The first of my catalogs whose {table}, its products or its factories, knows {decl}
        """
        # go through my catalogs, in order
        for catalog in self.catalogs:
            # if this one knows the type
            if decl in getattr(catalog, table):
                # it is the one
                return catalog
        # none of them does
        return None

    # metamethods
    def __init__(self, *, catalogs, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my catalogs, in the order they are searched
        self.catalogs = tuple(catalogs)
        # all done
        return


# end of file
