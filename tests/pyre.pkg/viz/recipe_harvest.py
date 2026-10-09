#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Describe a live flow as a recipe with every node pinned to its instance, and check that the
bindings made and undone through the recipe reach the instances
"""


def test():
    # support
    import pyre

    # a flow that computes magnitudes and normalizes them
    class Flow(pyre.flow.workflow, family="tests.pyre.viz.recipes.flow"):
        """
        The first two stages of the amplitude pipeline
        """

        # the operator
        operator = pyre.viz.operator()
        operator.default = pyre.viz.operators.amplitude
        # and the normalizer
        normalizer = pyre.viz.normalizer()

    # make one
    flow = Flow(name="flow")
    # make the tiles
    signal = pyre.viz.tiles.heap()(name="signal")
    magnitude = pyre.viz.tiles.heap()(name="magnitude")
    normalized = pyre.viz.tiles.heap()(name="normalized")
    # wire the operator
    flow.operator.signal = signal
    flow.operator.amplitude = magnitude
    # and the normalizer
    flow.normalizer.signal = magnitude
    flow.normalizer.normalized = normalized

    # describe the flow
    recipe = pyre.flow.recipe.harvest(flow=flow)
    # the factories are the ones of the flow, by name
    factories = {node.pin: node for node in recipe.factories()}
    # all of them
    assert set(map(id, factories)) == {id(flow.operator), id(flow.normalizer)}
    # pinned to their instances
    assert all(node.level == "instance" for node in recipe.nodes.values())
    # each factory satisfies the protocol it implements
    assert issubclass(factories[flow.operator].protocol, pyre.viz.operator)
    assert issubclass(factories[flow.normalizer].protocol, pyre.viz.normalizer)
    # the products are the tiles, each one once, however many slots it is bound to
    assert sorted(node.pin.pyre_name for node in recipe.products()) == [
        "magnitude",
        "normalized",
        "signal",
    ]
    # the names of the nodes of the factories
    operator = factories[flow.operator].name
    normalizer = factories[flow.normalizer].name
    # the magnitudes are written by the operator
    assert [b.factory for b in recipe.writers(product="magnitude")] == [operator]
    # and read by the normalizer
    assert [b.factory for b in recipe.readers(product="magnitude")] == [normalizer]
    # and must be magnitudes, since a tile on the heap does not say what it holds
    assert recipe.specification(product="magnitude") is pyre.viz.tiles.magnitude

    # undoing a binding of two instances
    recipe.unbind(factory=normalizer, slot="signal")
    # reaches the factory
    assert flow.normalizer.signal is None
    # and so does making one
    recipe.bind(factory=normalizer, slot="signal", product="magnitude")
    # which binds the tile
    assert flow.normalizer.signal is magnitude

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
