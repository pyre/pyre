#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Stage the amplitude recipe against the catalog of the extension: every factory gets the c++
engine that takes what its neighbors make, starting from the type of the signal; and check what
staging refuses
"""


# the amplitude recipe at the level of the protocols, with the operator and the colormap pinned
def amplitude():
    """
    Build the amplitude recipe
    """
    # support
    import pyre
    from pyre.viz.protocols.Unary import Unary

    # make a recipe
    recipe = pyre.flow.recipe()
    # the factories
    recipe.factory(name="amplitude", protocol=Unary, pin=pyre.viz.operators.amplitude())
    recipe.factory(name="normalizer", protocol=pyre.viz.normalizer, settings={"interval": (0, 10)})
    recipe.factory(name="gray", protocol=pyre.viz.colormap, pin=pyre.viz.colormaps.gray())
    recipe.factory(name="bmp", protocol=pyre.viz.encoder)
    # the products
    for name in ("signal", "magnitude", "normalized", "red", "green", "blue", "image"):
        # one at a time
        recipe.product(name=name)
    # the bindings
    for factory, slot, product in [
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
    import pyre
    from pyre.flow.exceptions import NoComponentError, NoEngineError, UnresolvedProductError
    from pyre.viz.protocols.Unary import Unary

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the tiles of complex samples and of doubles
    complex64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="complex64")
    float64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="float64")
    float32 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="float32")

    # stage the recipe, starting from complex samples
    plan = amplitude().stage(catalog=catalog, products={"signal": complex64})
    # every product has a type
    kinds = plan.kinds
    assert kinds["signal"] == complex64
    # the magnitudes are doubles, since that is what the amplitude engine makes
    assert kinds["magnitude"] == float64
    # and the colors are floats, which is what the colormap engine takes
    assert kinds["normalized"] == kinds["red"] == float32
    # the image is a bitmap
    assert kinds["image"] == "pyre::viz::products::images::bmp_t"
    # and every factory has the engine that fits
    assert kinds["amplitude"].startswith("pyre::flow::factories::selectors::amplitude_t<")
    assert kinds["normalizer"].startswith("pyre::flow::factories::filters::parametric_t<")
    assert kinds["gray"].startswith("pyre::viz::factories::colormaps::gray_t<")
    assert kinds["bmp"].startswith("pyre::viz::factories::codecs::bmp_t<")

    # a signal of doubles
    try:
        # leaves the amplitude with no engine that takes it
        amplitude().stage(catalog=catalog, products={"signal": float64})
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except NoEngineError as error:
        # that names the factory
        assert error.node == "amplitude"

    # a product the catalog cannot make
    try:
        # cannot be pinned
        amplitude().stage(catalog=catalog, products={"signal": "nonsense"})
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except UnresolvedProductError as error:
        # that names the product
        assert error.node == "signal"

    # a product bound to nothing
    recipe = amplitude()
    recipe.product(name="loose")
    try:
        # has no type
        recipe.stage(catalog=catalog, products={"signal": complex64})
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except UnresolvedProductError as error:
        # that names the product
        assert error.node == "loose"

    # a factory pinned to nothing, whose protocol has no default
    recipe = pyre.flow.recipe()
    recipe.factory(name="operator", protocol=Unary)
    try:
        # has no component to stage
        recipe.stage(catalog=catalog)
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except NoComponentError as error:
        # that names the factory
        assert error.node == "operator"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
