#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Pin the nodes of a recipe again, in place: a factory takes the slots of its new pin and loses the
bindings of the ones it no longer has, back down to its protocol and up to another class; a pin
that does not satisfy the protocol, or that would leave a slot clashing with its product, is
refused and leaves the node as it was
"""


def test():
    # support
    import pyre

    # the exceptions
    from pyre.flow.exceptions import IncompatibleBindingError, IncompatiblePinError

    # the classes to pin to
    amplitude = pyre.viz.operators.amplitude()  # one slot in, one out
    add = pyre.viz.operators.add()  # two in, one out

    # make a recipe
    recipe = pyre.flow.recipe()
    # with an operator that stands for any of them
    node = recipe.factory(name="op", protocol=pyre.viz.operator)
    # which has no slots of its own
    assert node.level == "protocol"
    # and so it has no slots
    assert node.slots == {}
    # and a product
    recipe.product(name="signal")

    # pin it to a class
    gone = recipe.pin(name="op", pin=amplitude)
    # which leaves no bindings behind, since it had none
    assert gone == []
    # and gives it the slots of the class
    assert node.level == "class"
    # whose slots it now has
    assert list(node.slots) == ["signal", "amplitude"]
    # so it can be bound
    recipe.bind(factory="op", slot="signal", product="signal")

    # pin it to a class with other slots
    gone = recipe.pin(name="op", pin=add)
    # its old slot is gone, and so is its binding
    assert [(b.factory, b.slot, b.product) for b in gone] == [("op", "signal", "signal")]
    # so the recipe has no bindings left
    assert recipe.bindings == []
    # and it has the new slots
    assert list(node.slots) == ["op1", "op2", "sum"]
    # bind one of them
    recipe.bind(factory="op", slot="op1", product="signal")

    # back to the protocol
    gone = recipe.pin(name="op", pin=None)
    # takes every slot along, with its binding
    assert [b.slot for b in gone] == ["op1"]
    # so the node stands for the protocol again
    assert node.level == "protocol"
    # and has no slots
    assert node.slots == {}

    # a class that does not satisfy the protocol
    try:
        # cannot be pinned
        recipe.pin(name="op", pin=pyre.viz.colormaps.gray())
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except IncompatiblePinError as error:
        # that names the node
        assert error.node == "op"
    # and the node is as it was
    assert node.pin is None

    # an amplitude
    recipe.factory(name="source", pin=amplitude)
    # a product of magnitudes
    recipe.product(name="magnitude")
    # written by the amplitude
    recipe.bind(factory="source", slot="amplitude", product="magnitude")

    # a selector that takes any tile
    recipe.factory(name="selector", protocol=pyre.viz.selector, pin=pyre.viz.selectors.real())
    # reads the magnitudes
    recipe.bind(factory="selector", slot="signal", product="magnitude")

    # a selector whose slot of the same name expects complex tiles, which magnitudes are not
    class Complex(
        pyre.flow.factory, family="tests.pyre.viz.selectors.complex", implements=pyre.viz.selector
    ):
        """
        A selector that reads complex tiles
        """

        # the input
        signal = pyre.viz.protocols.complex.input()
        # the output
        real = pyre.viz.tile.output()

    # so pinning the selector to it, which keeps the slot but changes what it expects
    try:
        # is refused
        recipe.pin(name="selector", pin=Complex)
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except IncompatibleBindingError as error:
        # that names the slot
        assert (error.node, error.slot, error.product) == ("selector", "signal", "magnitude")
    # and the selector is as it was, still bound
    assert recipe.node(name="selector").pin is pyre.viz.selectors.real()
    # and still reading the magnitudes
    assert recipe.binding(factory="selector", slot="signal").product == "magnitude"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
