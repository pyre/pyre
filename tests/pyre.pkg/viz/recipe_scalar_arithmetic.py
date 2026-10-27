#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Stage a recipe that adds, subtracts, multiplies and divides two scalars made by constants,
realize it, and check that every result is a scalar that holds the right value
"""


def test():
    # support
    import pyre

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the scalars of reals
    scalar = "pyre::flow::products::var_t<double>"
    # the operators, and the value each one makes of 6 and 4
    expected = {"add": 10, "subtract": 2, "multiply": 24, "divide": 1.5}

    # make a recipe
    recipe = pyre.flow.recipe()
    # the operands
    for name in ("x", "y"):
        # declared as scalars
        recipe.product(name=name, specification=pyre.viz.scalar)
    # the constants that make them
    for name, value in (("x", 6.0), ("y", 4.0)):
        # one at a time
        recipe.factory(
            name=f"{name}.value", pin=pyre.viz.filters.constant(), settings={"value": value}
        )
        # bound to its operand
        recipe.bind(factory=f"{name}.value", slot="result", product=name)
    # go through the operators
    for operator in expected:
        # its result
        recipe.product(name=f"{operator}.result")
        # the operator itself
        recipe.factory(name=operator, pin=getattr(pyre.viz.operators, operator)())
        # applied to the operands, in order
        for slot, product in (("op1", "x"), ("op2", "y"), ("result", f"{operator}.result")):
            # one binding at a time
            recipe.bind(factory=operator, slot=slot, product=product)

    # stage it; nothing is pinned, since the specifications of the operands decide
    plan = recipe.stage(catalog=catalog)
    # go through the operators
    for operator in expected:
        # each one is the arithmetic of scalars
        assert (
            plan.kinds[operator]
            == f"pyre::flow::factories::operators::{operator}_t<{scalar}, {scalar}, {scalar}>"
        ), plan.kinds[operator]
        # so its result is a scalar
        assert plan.kinds[f"{operator}.result"] == scalar

    # realize the plan; scalars have no shape, so any one does
    with plan.realize(shape=(1, 1)) as graph:
        # go through the operators
        for operator, value in expected.items():
            # and check the value of each result
            assert graph[f"{operator}.result"].value == value, operator

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
