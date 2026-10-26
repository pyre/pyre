#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Stage a recipe that adds two tiles of reals and subtracts one from the other, realize it, and
check that the engines the catalog picks compute the sum and the difference, in order
"""


def test():
    # support
    import pyre

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the tiles of reals
    float64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="float64")

    # make a recipe
    recipe = pyre.flow.recipe()
    # the products
    for name in ("a", "b", "sum", "difference"):
        # one at a time
        recipe.product(name=name)
    # the factories
    recipe.factory(name="add", pin=pyre.viz.operators.add())
    recipe.factory(name="subtract", pin=pyre.viz.operators.subtract())
    # the bindings
    for factory, slot, product in [
        ("add", "op1", "a"),
        ("add", "op2", "b"),
        ("add", "result", "sum"),
        ("subtract", "op1", "a"),
        ("subtract", "op2", "b"),
        ("subtract", "result", "difference"),
    ]:
        # one at a time
        recipe.bind(factory=factory, slot=slot, product=product)

    # stage it, starting from tiles of reals
    plan = recipe.stage(catalog=catalog, products={"a": float64, "b": float64})
    # the engines are the arithmetic of tiles of reals
    assert (
        plan.kinds["add"]
        == f"pyre::flow::factories::operators::add_t<{float64}, {float64}, {float64}>"
    )
    assert (
        plan.kinds["subtract"]
        == f"pyre::flow::factories::operators::subtract_t<{float64}, {float64}, {float64}>"
    )

    # the shape of the tiles
    shape = (3, 4)
    # realize the plan
    with plan.realize(shape=shape) as graph:
        # get the cells of the operands
        a = graph["a"].write()
        b = graph["b"].write()
        # go through them
        for i in range(shape[0]):
            for j in range(shape[1]):
                # and fill them with values that tell the cells apart
                a[i, j] = 10 * i + j
                b[i, j] = 0.5 * j
        # pull the results
        total = graph["sum"].read()
        difference = graph["difference"].read()
        # go through their cells
        for i in range(shape[0]):
            for j in range(shape[1]):
                # the sum
                assert total[i, j] == 10 * i + 1.5 * j
                # and the difference, which respects the order of the operands
                assert difference[i, j] == 10 * i + 0.5 * j

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
