#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Realize the staged amplitude recipe for two tile shapes, and check that its image matches, byte
for byte, the one of the graph the c++ driver {amplitude_catalog} builds from the catalog by hand,
which matches the hand built pipeline of {amplitude_pipeline}
"""


# the graph {amplitude_catalog} builds, wired by hand through the catalog
def byHand(*, catalog, shape: tuple) -> dict:
    """
    Make and wire the amplitude pipeline for tiles of the given {shape} the way the c++ driver
    does, naming every type
    """
    # support
    import pyre

    # the tiles
    tile = pyre.flow.recipes.plan.tile
    complex64 = tile(catalog=catalog, cell="complex64")
    float64 = tile(catalog=catalog, cell="float64")
    float32 = tile(catalog=catalog, cell="float32")
    # the factories, by readable name
    entries = {e.className: e.decl for e in catalog.factories.values()}
    # the products
    nodes = {
        "signal": catalog.makeProduct(decl=complex64, name="signal", shape=shape),
        "magnitude": catalog.makeProduct(decl=float64, name="magnitude", shape=shape),
        "normalized": catalog.makeProduct(decl=float32, name="normalized", shape=shape),
        "red": catalog.makeProduct(decl=float32, name="red", shape=shape),
        "green": catalog.makeProduct(decl=float32, name="green", shape=shape),
        "blue": catalog.makeProduct(decl=float32, name="blue", shape=shape),
        "image": catalog.makeProduct(
            decl="pyre::viz::products::images::bmp_t", name="image", shape=shape
        ),
    }
    # the factories
    for name, kind in [
        ("amplitude", "Amplitude"),
        ("normalizer", "Parametric"),
        ("gray", "Gray"),
        ("bmp", "BMP"),
    ]:
        # one at a time
        nodes[name] = catalog.makeFactory(decl=entries[kind], name=name)
    # the interval of the normalizer
    nodes["normalizer"].set(setting="interval", value=(0, 10))
    # the wiring
    for factory, slot, product in BINDINGS:
        # one binding at a time
        assert nodes[factory].bind(slot=slot, product=nodes[product])
    # hand off the graph
    return nodes


# the bindings of the amplitude pipeline
BINDINGS = [
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
]


# fill a signal with magnitudes 0, 1, 2, ... at phases that vary with the cell
def fill(*, signal, shape: tuple) -> None:
    """
    Fill {signal}, a tile of the given {shape}, the same way every time
    """
    # support
    import cmath

    # unpack
    lines, samples = shape
    # get the cells, which marks what depends on them as stale
    cells = signal.write()
    # one line at a time
    for i in range(lines):
        # and one sample at a time
        for j in range(samples):
            # the cell number
            cell = i * samples + j
            # the value
            cells[i, j] = cmath.rect(cell % 50, 0.1 * cell)
    # all done
    return


def test():
    # support
    import pyre

    # the recipe
    from recipe_staging import amplitude

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the tiles of complex samples
    complex64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="complex64")
    # stage the recipe, starting from complex samples
    plan = amplitude().stage(catalog=catalog, products={"signal": complex64})

    # realize it for two shapes
    for shape in [(8, 8), (5, 13)]:
        # the graph of the plan
        with plan.realize(shape=shape) as graph:
            # every factory knows the family of the component it stands for, which names the
            # debug channel its work is reported on
            assert graph["amplitude"].family == "pyre.viz.operators.amplitude"
            assert graph["normalizer"].family == "pyre.viz.normalizers.parametric"
            assert graph["gray"].family == "pyre.viz.colormaps.gray"
            assert graph["bmp"].family == "pyre.viz.encoders.bmp"
            # fill its signal
            fill(signal=graph["signal"], shape=shape)
            # and pull its image
            staged = graph["image"].read()
        # the graph wired by hand
        nodes = byHand(catalog=catalog, shape=shape)
        # fill its signal the same way
        fill(signal=nodes["signal"], shape=shape)
        # and pull its image
        expected = nodes["image"].read()
        # take it apart
        for factory, slot, _ in BINDINGS:
            # one binding at a time
            nodes[factory].unbind(slot=slot)
        # the two images match, byte for byte
        assert staged == expected

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
