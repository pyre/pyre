#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The nodes of a flow keep the names the framework gives them: the factories and products a named
flow makes for itself are named after it, and the ones of an anonymous flow have no names, can be
wired all the same, and are named after their roles in the flow once it is described as a recipe
"""


def test() -> None:
    """
    Build a named and an anonymous flow, wire them, and describe them as recipes
    """
    # support
    import pyre

    # a flow that computes magnitudes and normalizes them
    class Flow(pyre.flow.workflow, family="tests.pyre.viz.recipes.names"):
        """
        The first two stages of the amplitude pipeline
        """

        # the operator
        operator = pyre.viz.operator()
        operator.default = pyre.viz.operators.amplitude
        # and the normalizer
        normalizer = pyre.viz.normalizer()

        # framework hooks
        def pyre_configured(self, **kwds):
            """
            Wire the normalizer to the output of the operator
            """
            # the normalizer reads the magnitudes
            self.normalizer.signal = self.operator.amplitude
            # chain up
            return super().pyre_configured(**kwds)

    # a named flow
    named = Flow(name="names")
    # names the factories it makes for itself after itself: the operator
    assert named.operator.pyre_name == "names.operator", named.operator.pyre_name
    # and the normalizer
    assert named.normalizer.pyre_name == "names.normalizer", named.normalizer.pyre_name
    # and their products after them
    assert named.operator.amplitude.pyre_name == "names.operator.amplitude"
    # it is wired
    assert named.normalizer.signal is named.operator.amplitude
    # except for the input of the operator, which is bound to nothing so it holds nothing
    assert named.operator.signal is None
    # and its recipe
    recipe = pyre.flow.recipe.harvest(flow=named)
    # uses the names of its nodes, with none for what the operator reads
    assert sorted(recipe.nodes) == [
        "names.normalizer",
        "names.normalizer.normalized",
        "names.operator",
        "names.operator.amplitude",
    ], sorted(recipe.nodes)

    # an anonymous flow
    anonymous = Flow()
    # has nodes with no names: its factories
    assert anonymous.operator.pyre_name is None, anonymous.operator.pyre_name
    # and their products
    assert anonymous.operator.amplitude.pyre_name is None
    # that are wired all the same
    assert anonymous.normalizer.signal is anonymous.operator.amplitude
    # and can be wired again
    anonymous.normalizer.signal = named.operator.amplitude
    # to products of another flow
    assert anonymous.normalizer.signal is named.operator.amplitude
    # put it back
    anonymous.normalizer.signal = anonymous.operator.amplitude
    # its recipe
    recipe = pyre.flow.recipe.harvest(flow=anonymous)
    # names the factories after their roles, and the products they make for themselves after
    # the factory and the slot
    assert sorted(recipe.nodes) == [
        "normalizer",
        "normalizer.normalized",
        "operator",
        "operator.amplitude",
    ], sorted(recipe.nodes)
    # the product the two share is one node, written by the operator
    assert [b.factory for b in recipe.writers(product="operator.amplitude")] == ["operator"]
    # and read by the normalizer
    assert [b.factory for b in recipe.readers(product="operator.amplitude")] == ["normalizer"]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
