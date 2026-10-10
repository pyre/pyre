#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Stage a recipe whose head is a reader that computes in python: staging runs it first, so the
raster it exposes decides which slice fits, and every graph the plan realizes reads that raster;
the tiles match the ones the same recipe renders from a raster handed in by hand
"""


def test():
    # support
    import cmath
    import pyre

    # the recipe with a slice at its head, which starts at a raster
    from recipe_slice import sliced

    # a reader that exposes the cells of a grid it holds
    class Grid(pyre.flow.factory, family="tests.pyre.viz.readers.grid", implements=pyre.viz.reader):
        """
        A reader of a grid in memory
        """

        # the location of the file, which a reader of memory ignores
        uri = pyre.properties.uri()
        uri.doc = "where the cells would come from"

        # the output
        raster = pyre.viz.raster.output()
        raster.doc = "the cells of the grid"

        # flow hooks
        def pyre_stage(self, **inputs) -> dict:
            """
            Expose the cells of my grid as a raster
            """
            # count my runs
            self.runs += 1
            # make the raster and hand it off
            return {"raster": pyre.libpyre.flow.raster(source=self.cells, name="grid")}

        # metamethods
        def __init__(self, cells=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # the cells
            self.cells = cells
            # and the number of times i was staged
            self.runs = 0
            # all done
            return

    # a grid of complex values
    lines, samples = 24, 30
    cells = pyre.libpyre.grid.heap(shape=[lines, samples], cell="complex64")
    # filled with magnitudes that wrap around every 11 cells, at phases that vary with the cell
    for line in range(lines):
        # one sample at a time
        for sample in range(samples):
            # the cell number
            cell = line * samples + sample
            # the value
            cells[line, sample] = cmath.rect(cell % 11, 0.2 * cell)
    # a reader of it
    reader = Grid(name="tests.pyre.viz.recipe_reader.grid", cells=cells)

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the recipe with a reader in front of the slice
    recipe = sliced()
    recipe.factory(name="reader", protocol=pyre.viz.reader, pin=reader)
    recipe.bind(factory="reader", slot="raster", product="raster")
    # stage it, which runs the reader
    plan = recipe.stage(catalog=catalog)
    # once
    assert reader.runs == 1
    # its raster is what the slice reads
    assert plan.kinds["raster"] == pyre.flow.recipes.plan.raster(catalog=catalog, cell="complex64")

    # the same recipe without the reader, its raster handed in by hand
    manual = sliced().stage(catalog=catalog, products={"raster": plan.kinds["raster"]})
    source = pyre.libpyre.flow.raster(source=cells, name="raster")

    # render two tiles of different shapes, each from a graph of its own
    for shape, origin, stride in [((6, 6), (1, 1), (2, 2)), ((4, 9), (0, 2), (3, 1))]:
        # the graph of the plan, whose raster the reader made
        with plan.realize(shape=shape) as graph:
            # move the window
            graph["slice"].set(setting="origin", value=origin)
            graph["slice"].set(setting="stride", value=stride)
            # and pull the image
            staged = graph["image"].read()
        # the graph whose raster was handed in
        with manual.realize(shape=shape, nodes={"raster": source}) as graph:
            # the same window
            graph["slice"].set(setting="origin", value=origin)
            graph["slice"].set(setting="stride", value=stride)
            # and pull its image
            expected = graph["image"].read()
        # they match, byte for byte
        assert staged == expected, (shape, origin, stride)
    # and the reader ran only when the recipe was staged
    assert reader.runs == 1

    # a reader nobody implements cannot be staged
    from pyre.flow.exceptions import NoComponentError

    # a recipe with an unpinned reader
    recipe = sliced()
    recipe.factory(name="reader", protocol=pyre.viz.reader)
    recipe.bind(factory="reader", slot="raster", product="raster")
    try:
        # cannot be staged
        recipe.stage(catalog=catalog)
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except NoComponentError as error:
        # that names the reader
        assert error.node == "reader"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
