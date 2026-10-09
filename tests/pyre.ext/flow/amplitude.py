#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Realize the amplitude pipeline from python, through the catalog and the generic bindings alone,
for two tile shapes, and pull an image out of each one
"""

# the recipe: the kinds of the factories, by readable name, and the bindings
FACTORIES = {
    "amplitude": "Amplitude",
    "normalizer": "Parametric",
    "gray": "Gray",
    "bmp": "BMP",
}
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


def realize(*, catalog, shape: tuple) -> dict:
    """
    Make the nodes of the amplitude pipeline for tiles of the given {shape}, and wire them
    """
    # the entries of the factories, by readable name
    entries = {e.className: e for e in catalog.factories.values()}
    # make the factories
    nodes = {
        name: catalog.makeFactory(decl=entries[kind].decl, name=name)
        for name, kind in FACTORIES.items()
    }
    # the normalizer maps [0,10] onto [0,1]
    nodes["normalizer"].set(setting="interval", value=(0, 10))
    # go through the bindings
    for factory, slot, product in BINDINGS:
        # make each product the first time it comes up, of the type its writer or first
        # reader takes
        if product not in nodes:
            # find the description of the slot
            (description,) = [s for s in nodes[factory].slots if s.name == slot]
            # and make the product it takes
            nodes[product] = catalog.makeProduct(
                decl=description.product, name=product, shape=shape
            )
        # bind it
        assert nodes[factory].bind(slot=slot, product=nodes[product])
    # hand off the graph
    return nodes


def test():
    # support
    import cmath

    # the flow bindings
    from pyre.extensions.pyre import flow

    # get the catalog
    catalog = flow.catalog()
    # realize the pipeline for two shapes
    for lines, samples in [(8, 8), (5, 13)]:
        # build the graph
        nodes = realize(catalog=catalog, shape=(lines, samples))
        # fill the signal
        cells = nodes["signal"].write()
        # one line at a time
        for i in range(lines):
            # and one sample at a time
            for j in range(samples):
                # the cell number
                cell = i * samples + j
                # magnitudes 0, 1, 2, ... at phases that vary with the cell
                cells[i, j] = cmath.rect(cell % 50, 0.1 * cell)
        # pull the image
        image = nodes["image"].read()
        # it is a bitmap
        assert image[:2] == b"BM"
        # whose header records its own size
        assert int.from_bytes(image[2:6], "little") == len(image)
        # its width and its height
        assert int.from_bytes(image[18:22], "little", signed=True) == samples
        assert abs(int.from_bytes(image[22:26], "little", signed=True)) == lines
        # and the magnitudes are painted: the first cell has magnitude 0, painted black
        payload = image[54:]
        # in one of the corners of the image, depending on which way the lines run
        assert payload[:3] == b"\x00\x00\x00" or image[-3:] == b"\x00\x00\x00"
        # take the graph apart
        for factory, slot, _ in BINDINGS:
            # one binding at a time
            nodes[factory].unbind(slot=slot)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
