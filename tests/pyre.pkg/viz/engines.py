#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the components of pyre.viz and the catalog of the extension agree: every c++ template a
component names as its engine has instantiations in the catalog, and every factory in the catalog
instantiates a template some component names
"""


def test():
    # support
    import pyre

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the templates the catalog has instantiations of
    instantiated = {entry.decl.split("<", 1)[0] for entry in catalog.factories.values()}

    # the categories of factories
    categories = [
        pyre.viz.selector,
        pyre.viz.operator,
        pyre.viz.normalizer,
        pyre.viz.filter,
        pyre.viz.colormap,
        pyre.viz.encoder,
        pyre.viz.slicer,
    ]
    # the templates the components name, by component
    named = {}
    # go through the categories
    for category in categories:
        # and their implementers
        for _, _, implementer in category.pyre_locateAllImplementers(namespace="pyre"):
            # a foundry hands out the class it stands for
            cls = implementer() if isinstance(implementer, pyre.foundry) else implementer
            # record what it names
            named[cls.pyre_family()] = set(cls.pyre_engines)

    # every template a component names
    for family, templates in named.items():
        # has instantiations in the catalog
        assert templates <= instantiated, (family, templates - instantiated)
    # and every template in the catalog is named by some component
    claimed = set().union(*named.values())
    assert instantiated <= claimed, instantiated - claimed

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
