#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Stage a recipe in which a constant makes a scalar that shifts, scales and divides a tile of
reals, on either side where the math allows it; realize it, check the cells, and check that a
new value for the constant reaches every result
"""


def test():
    # support
    import pyre

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the tiles of reals
    float64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="float64")
    # the scalars of reals
    scalar = "pyre::flow::products::var_t<double>"

    # make a recipe
    recipe = pyre.flow.recipe()
    # the tile
    recipe.product(name="tile")
    # the scalar, which is what makes it a scalar rather than a constant tile
    recipe.product(name="scale", specification=pyre.viz.scalar)
    # and the results
    for name in ("shifted", "negated", "scaled", "quotient"):
        # one at a time
        recipe.product(name=name)
    # the factory of the scalar
    recipe.factory(name="constant", pin=pyre.viz.filters.constant(), settings={"value": 4.0})
    # the sum of the tile and the scalar
    recipe.factory(name="add", pin=pyre.viz.operators.add())
    # the scalar less the tile
    recipe.factory(name="subtract", pin=pyre.viz.operators.subtract())
    # the tile scaled by the scalar on its left
    recipe.factory(name="multiply", pin=pyre.viz.operators.multiply())
    # and the tile divided by the scalar
    recipe.factory(name="divide", pin=pyre.viz.operators.divide())
    # the bindings
    for factory, slot, product in [
        ("constant", "result", "scale"),
        ("add", "op1", "tile"),
        ("add", "op2", "scale"),
        ("add", "result", "shifted"),
        ("subtract", "op1", "scale"),
        ("subtract", "op2", "tile"),
        ("subtract", "result", "negated"),
        ("multiply", "op1", "scale"),
        ("multiply", "op2", "tile"),
        ("multiply", "result", "scaled"),
        ("divide", "op1", "tile"),
        ("divide", "op2", "scale"),
        ("divide", "result", "quotient"),
    ]:
        # one at a time
        recipe.bind(factory=factory, slot=slot, product=product)

    # stage it, starting from a tile of reals
    plan = recipe.stage(catalog=catalog, products={"tile": float64})
    # the scalar is a scalar, as its specification says
    assert plan.kinds["scale"] == scalar
    # made by a constant scalar
    assert plan.kinds["constant"] == f"pyre::flow::factories::filters::constant_t<{scalar}>"
    # the results are tiles
    for name in ("shifted", "negated", "scaled", "quotient"):
        # one at a time
        assert plan.kinds[name] == float64, name
    # and the engines put the scalar on the side the recipe binds it to
    assert (
        plan.kinds["subtract"]
        == f"pyre::flow::factories::operators::subtract_t<{scalar}, {float64}, {float64}>"
    )
    # with the tile first when it comes first
    assert (
        plan.kinds["divide"]
        == f"pyre::flow::factories::operators::divide_t<{float64}, {scalar}, {float64}>"
    )

    # the shape of the tiles
    shape = (3, 4)
    # realize the plan
    with plan.realize(shape=shape) as graph:
        # get the cells of the tile
        cells = graph["tile"].write()
        # go through its lines
        for i in range(shape[0]):
            # and its samples
            for j in range(shape[1]):
                # and fill them with values that tell the cells apart
                cells[i, j] = 10 * i + j
        # the scalar holds the value of the constant
        assert graph["scale"].value == 4
        # check the results for a value of the constant
        check(graph=graph, shape=shape, value=4)
        # give the constant a new value
        assert graph["constant"].set(setting="value", value=2.0)
        # which reaches the scalar
        assert graph["scale"].value == 2
        # and every result computed from it
        check(graph=graph, shape=shape, value=2)

    # all done
    return


def check(*, graph, shape: tuple, value: float) -> None:
    """
    Check the cells of the results of {graph}, whose scalar has the given {value}
    """
    # pull the results
    shifted = graph["shifted"].read()
    # all of them
    negated = graph["negated"].read()
    scaled = graph["scaled"].read()
    quotient = graph["quotient"].read()
    # go through their lines
    for i in range(shape[0]):
        # and their samples
        for j in range(shape[1]):
            # the cell of the tile
            cell = 10 * i + j
            # the sum
            assert shifted[i, j] == cell + value
            # the difference, which respects the order of the operands
            assert negated[i, j] == value - cell
            # the product
            assert scaled[i, j] == value * cell
            # and the quotient
            assert quotient[i, j] == cell / value
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
