#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Build the amplitude recipe at the level of the protocols, with the colormap pinned to the gray
class, and check the slots of its factories, its bindings, and what its products must hold
"""


def test():
    # support
    import pyre

    # the specifications
    tiles = pyre.viz.tiles
    # the building block of the unary operators
    from pyre.viz.protocols.Unary import Unary

    # make a recipe
    recipe = pyre.flow.recipe()

    # the products, none of them declared with a specification
    for name in ("signal", "magnitude", "normalized", "red", "green", "blue", "image"):
        # add each one
        recipe.product(name=name)
    # the factories: an operator that satisfies the unary protocol
    recipe.factory(name="amplitude", protocol=Unary, pin=pyre.viz.operators.amplitude())
    # a normalizer, with the interval it will be made with
    recipe.factory(name="normalizer", protocol=pyre.viz.normalizer, settings={"interval": (0, 10)})
    # a colormap, pinned to the gray class
    recipe.factory(name="gray", protocol=pyre.viz.colormap, pin=pyre.viz.colormaps.gray())
    # and an encoder
    recipe.factory(name="bmp", protocol=pyre.viz.encoder)

    # the levels
    assert recipe.node(name="signal").level == "protocol"
    assert recipe.node(name="amplitude").level == "class"
    assert recipe.node(name="normalizer").level == "protocol"
    assert recipe.node(name="gray").level == "class"
    assert recipe.node(name="bmp").level == "protocol"
    # the settings travel with the node until it is made
    assert recipe.node(name="normalizer").settings == {"interval": (0, 10)}

    # the slots of a factory pinned to a class are the ones of the class
    assert list(recipe.node(name="amplitude").slots) == ["signal", "amplitude"]
    # the ones of a factory that is not pinned are the ones its protocol declares
    assert list(recipe.node(name="normalizer").slots) == ["signal", "normalized"]
    assert list(recipe.node(name="bmp").slots) == ["red", "green", "blue", "image"]
    # so pinning the colormap to gray adds the input the protocol leaves to its colormaps
    gray = recipe.node(name="gray")
    # by direction
    assert [trait.name for trait in gray.inputs] == ["data"]
    assert [trait.name for trait in gray.outputs] == ["red", "green", "blue"]
    # an unpinned colormap has only the outputs
    colormap = pyre.flow.recipes.factory(name="colormap", protocol=pyre.viz.colormap)
    assert list(colormap.slots) == ["red", "green", "blue"]

    # the bindings, the same as the c++ recipe, slot names and all
    bindings = [
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
    # make them
    for factory, slot, product in bindings:
        # one at a time
        recipe.bind(factory=factory, slot=slot, product=product)
    # they are all there, in order
    assert [tuple(binding) for binding in recipe.bindings] == bindings

    # the magnitudes are written by the amplitude and read by the normalizer
    assert [b.factory for b in recipe.writers(product="magnitude")] == ["amplitude"]
    assert [b.factory for b in recipe.readers(product="magnitude")] == ["normalizer"]
    # and must be what the most demanding of their slots expects
    assert recipe.specification(product="magnitude") is tiles.magnitude
    # the signal is complex
    assert recipe.specification(product="signal") is tiles.complex
    # the normalized values are unit values
    assert recipe.specification(product="normalized") is tiles.unit
    # the color channels are color channels
    assert recipe.specification(product="red") is tiles.channel
    # and the image is a raster
    assert recipe.specification(product="image") is pyre.viz.raster

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
