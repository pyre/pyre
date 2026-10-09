#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Stage the amplitude recipe with a slice at its head, so its data come from a raster through the
graph itself, and check that every tile it renders matches, byte for byte, the one the amplitude
recipe renders from the same window copied in by hand
"""


# the amplitude recipe, with a slice reading a raster in front of it
def sliced():
    """
    Build the amplitude recipe that starts at a raster
    """
    # support
    import pyre
    from pyre.viz.protocols.Unary import Unary

    # make a recipe
    recipe = pyre.flow.recipe()
    # the factories
    recipe.factory(name="slice", protocol=pyre.viz.slicer)
    recipe.factory(name="amplitude", protocol=Unary, pin=pyre.viz.operators.amplitude())
    recipe.factory(name="normalizer", protocol=pyre.viz.normalizer, settings={"interval": (0, 10)})
    recipe.factory(name="gray", protocol=pyre.viz.colormap, pin=pyre.viz.colormaps.gray())
    recipe.factory(name="bmp", protocol=pyre.viz.encoder)
    # the products
    for name in ("raster", "signal", "magnitude", "normalized", "red", "green", "blue", "image"):
        # one at a time
        recipe.product(name=name)
    # the bindings
    for factory, slot, product in [
        ("slice", "source", "raster"),
        ("slice", "slice", "signal"),
        ("amplitude", "signal", "signal"),
        ("amplitude", "amplitude", "magnitude"),
        ("normalizer", "signal", "magnitude"),
        ("normalizer", "normalized", "normalized"),
        ("gray", "data", "normalized"),
        ("gray", "red", "red"),
        ("gray", "green", "green"),
        ("gray", "blue", "blue"),
        ("bmp", "red", "red"),
        ("bmp", "green", "green"),
        ("bmp", "blue", "blue"),
        ("bmp", "image", "image"),
    ]:
        # one at a time
        recipe.bind(factory=factory, slot=slot, product=product)
    # hand it off
    return recipe


def test():
    # support
    import cmath
    import pyre

    # the recipe without the slice, whose signal is filled by hand
    from recipe_staging import amplitude

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the types of the sources
    raster = pyre.flow.recipes.plan.raster(catalog=catalog, cell="complex64")
    complex64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="complex64")

    # a raster of complex values
    lines, samples = 40, 50
    cells = pyre.libpyre.grid.heap(shape=[lines, samples], cell="complex64")
    # filled with magnitudes that wrap around every 13 cells, at phases that vary with the cell
    for line in range(lines):
        # one sample at a time
        for sample in range(samples):
            # the cell number
            cell = line * samples + sample
            # the value
            cells[line, sample] = cmath.rect(cell % 13, 0.1 * cell)
    # a raster over the cells
    source = pyre.libpyre.flow.raster(source=cells, name="raster")

    # stage the recipe with the slice, starting from the raster
    plan = sliced().stage(catalog=catalog, products={"raster": raster})
    # the slice is the one that reads complex rasters into tiles of the same cells
    assert plan.kinds["signal"] == complex64
    # and stage the one without it, starting from the tiles
    manual = amplitude().stage(catalog=catalog, products={"signal": complex64})

    # the tiles to render: their shape, their origin counted in strides, and their stride
    tiles = [((8, 8), (0, 0), (1, 1)), ((5, 13), (2, 1), (2, 3)), ((8, 8), (1, 2), (4, 2))]
    # one shape at a time, each with a graph of its own
    for shape, origin, stride in tiles:
        # unpack
        rows, columns = shape
        # realize the recipe with the slice, the raster made elsewhere
        with plan.realize(shape=shape, nodes={"raster": source}) as graph:
            # move the window
            graph["slice"].set(setting="origin", value=origin)
            graph["slice"].set(setting="stride", value=stride)
            # and pull the image
            sliced_image = graph["image"].read()
        # realize the recipe without it
        with manual.realize(shape=shape) as graph:
            # copy the same window into the signal by hand
            signal = graph["signal"].write()
            # one row at a time
            for row in range(rows):
                # and one column at a time
                for column in range(columns):
                    # the cell of the raster that lands here
                    signal[row, column] = cells[
                        (origin[0] + row) * stride[0], (origin[1] + column) * stride[1]
                    ]
            # and pull the image
            manual_image = graph["image"].read()
        # the two images match, byte for byte
        assert sliced_image == manual_image, (shape, origin, stride)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
