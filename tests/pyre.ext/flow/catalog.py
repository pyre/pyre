#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the catalog of the extension knows the kinds of nodes it was compiled with, under the
spellings of their types, and describes them before any node of their kind exists
"""


def test():
    # the flow bindings
    from pyre.extensions.pyre import flow

    # get the catalog
    catalog = flow.catalog()
    # it is the one catalog
    assert flow.catalog() is catalog

    # the spelling of the tile of doubles
    float64 = (
        "pyre::flow::products::tile_t<pyre::grid::grid_t<"
        "pyre::grid::canonical_t<2>, pyre::memory::heap_t<double>>>"
    )
    # the catalog knows it
    tile = catalog.products[float64]
    # under its spelling
    assert tile.decl == float64
    # with its readable name
    assert tile.className == "TileGridCanonical2DHeapDouble"
    # and the spelling of its cells
    assert tile.cell == "double"
    # it knows the image too
    image = catalog.products["pyre::viz::products::images::bmp_t"]
    # which has no cells
    assert image.cell == ""

    # find the normalizer among the factories
    (normalizer,) = [e for e in catalog.factories.values() if e.className == "Parametric"]
    # its slots, before any normalizer exists
    assert [slot.name for slot in normalizer.slots] == ["signal", "normalized"]
    # an input
    assert normalizer.slots[0].reads and not normalizer.slots[0].writes
    # that takes tiles of doubles
    assert normalizer.slots[0].product == float64
    # an output
    assert normalizer.slots[1].writes
    # whose products the catalog knows as well
    assert normalizer.slots[1].product in catalog.products
    # and its settings
    assert [(s.name, s.type) for s in normalizer.settings] == [("interval", "interval")]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
