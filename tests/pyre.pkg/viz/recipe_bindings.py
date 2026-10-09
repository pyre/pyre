#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check what a recipe refuses: names it has already, nodes and slots it does not have, pins that
do not satisfy their protocol, and bindings that join unrelated specifications; and that binding
a slot again replaces its binding, and removing a node takes its bindings along
"""


def test():
    # support
    import pyre

    # the exceptions
    from pyre.flow.exceptions import (
        DuplicateNodeError,
        IncompatibleBindingError,
        IncompatiblePinError,
        UnknownNodeError,
        UnknownSlotError,
    )

    # make a recipe
    recipe = pyre.flow.recipe()
    # with a few products
    recipe.product(name="magnitude")
    recipe.product(name="other")
    # and factories
    recipe.factory(name="amplitude", pin=pyre.viz.operators.amplitude())
    recipe.factory(name="gray", pin=pyre.viz.colormaps.gray())

    # a name that is taken
    try:
        # cannot be used again, even for a node of the other kind
        recipe.factory(name="magnitude", protocol=pyre.viz.normalizer)
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except DuplicateNodeError as error:
        # that names the node
        assert error.node == "magnitude"

    # a pin that does not satisfy the protocol
    try:
        # cannot stand in for it
        recipe.factory(name="colormap", protocol=pyre.viz.colormap, pin=pyre.viz.encoders.bmp())
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except IncompatiblePinError as error:
        # that names the node
        assert error.node == "colormap"
    # and leaves no node behind
    assert "colormap" not in recipe.nodes

    # a node that is not there
    try:
        # cannot be bound
        recipe.bind(factory="nobody", slot="signal", product="magnitude")
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except UnknownNodeError as error:
        # that names the node
        assert error.node == "nobody"
    # nor can a product stand in for a factory
    try:
        # by binding through it
        recipe.bind(factory="magnitude", slot="signal", product="other")
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except UnknownNodeError as error:
        # that names the node
        assert error.node == "magnitude"
    # a slot that is not there
    try:
        # cannot be bound either
        recipe.bind(factory="amplitude", slot="data", product="magnitude")
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except UnknownSlotError as error:
        # that names the factory and the slot
        assert (error.node, error.slot) == ("amplitude", "data")

    # the amplitude writes magnitudes
    recipe.bind(factory="amplitude", slot="amplitude", product="magnitude")
    # which are not unit values, nor the other way around, so gray cannot read them
    try:
        # as its data
        recipe.bind(factory="gray", slot="data", product="magnitude")
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except IncompatibleBindingError as error:
        # that names both specifications
        assert error.expected is pyre.viz.tiles.unit
        assert error.offered is pyre.viz.tiles.magnitude
    # and leaves the bindings as they were
    assert [tuple(b) for b in recipe.bindings] == [("amplitude", "amplitude", "magnitude")]

    # binding the slot again
    recipe.bind(factory="amplitude", slot="amplitude", product="other")
    # replaces its binding
    assert [tuple(b) for b in recipe.bindings] == [("amplitude", "amplitude", "other")]
    # and a binding that is undone
    assert recipe.unbind(factory="amplitude", slot="amplitude").product == "other"
    # is gone
    assert recipe.binding(factory="amplitude", slot="amplitude") is None
    # undoing it again does nothing
    assert recipe.unbind(factory="amplitude", slot="amplitude") is None

    # bind the product again
    recipe.bind(factory="amplitude", slot="amplitude", product="magnitude")
    # remove the product
    recipe.remove(name="magnitude")
    # which takes its binding along
    assert recipe.bindings == []
    # and the node
    assert "magnitude" not in recipe.nodes

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
