#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that staging refuses what the math does not allow: the product or the quotient of two
tiles, a quotient by a tile, and a scalar pinned to the type of a tile; and that binding a scalar
to a slot that expects a tile is refused before staging
"""


def test():
    # support
    import pyre

    # the exceptions
    from pyre.flow.exceptions import (
        IncompatibleBindingError,
        NoEngineError,
        UnresolvedProductError,
    )

    # the catalog
    catalog = pyre.libpyre.flow.catalog()
    # the tiles of reals
    float64 = pyre.flow.recipes.plan.tile(catalog=catalog, cell="float64")

    # the operators the math restricts, and the operands each one refuses, as tile or scalar
    cases = [
        # the product of two tiles
        ("multiply", "tile", "tile"),
        # their quotient
        ("divide", "tile", "tile"),
        # and a scalar divided by a tile
        ("divide", "scalar", "tile"),
    ]
    # go through them
    for operator, first, second in cases:
        # make a recipe
        recipe = binary(pyre=pyre, operator=operator, first=first, second=second)
        # the tiles among the operands
        tiles = {name: float64 for name, kind in (("a", first), ("b", second)) if kind == "tile"}
        # staging it
        try:
            # should fail
            recipe.stage(catalog=catalog, products=tiles)
            # so getting here is an error
            assert False, (operator, first, second)
        # because no engine takes the operands
        except NoEngineError as error:
            # and the error says which factory could not be placed
            assert error.node == operator, (operator, error.node)

    # a scalar
    recipe = binary(pyre=pyre, operator="add", first="scalar", second="tile")
    # pinned to the type of a tile
    try:
        # should fail
        recipe.stage(catalog=catalog, products={"a": float64, "b": float64})
        # so getting here is an error
        assert False, "a scalar was pinned to the type of a tile"
    # because its specification rules the type out
    except UnresolvedProductError as error:
        # and the error names the product
        assert error.node == "a", error.node

    # make a recipe
    recipe = pyre.flow.recipe()
    # with a scalar
    recipe.product(name="scale", specification=pyre.viz.scalar)
    # and the amplitude, which reads complex tiles
    recipe.factory(name="amplitude", pin=pyre.viz.operators.amplitude())
    # binding the scalar to it
    try:
        # should fail
        recipe.bind(factory="amplitude", slot="signal", product="scale")
        # so getting here is an error
        assert False, "a scalar was bound to a slot that expects a tile"
    # because a scalar is no tile
    except IncompatibleBindingError:
        # as expected
        pass

    # all done
    return


def binary(*, pyre, operator: str, first: str, second: str):
    """
    Make a recipe that applies {operator} to the operands {a} and {b}, which are of the kinds
    {first} and {second}
    """
    # make a recipe
    recipe = pyre.flow.recipe()
    # the operands
    for name, kind in (("a", first), ("b", second)):
        # declared by kind
        recipe.product(name=name, specification=getattr(pyre.viz, kind))
    # the result
    recipe.product(name="result")
    # the operator
    recipe.factory(name=operator, pin=getattr(pyre.viz.operators, operator)())
    # the bindings
    for slot, product in (("op1", "a"), ("op2", "b"), ("result", "result")):
        # one at a time
        recipe.bind(factory=operator, slot=slot, product=product)
    # hand off the recipe
    return recipe


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
