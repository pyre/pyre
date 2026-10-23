#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a list or a tuple of components that is handed a component class holds an instance
of it with no name, one for the class and one for each instance, and that a specification with a
name still names its instance
"""

# support
import pyre


# a protocol for the entries
class Widget(pyre.protocol, family="pyre.tests.sequences.anonymous.widgets"):
    """
    What the sequences hold
    """


# an implementation
class Gadget(
    pyre.component, family="pyre.tests.sequences.anonymous.widgets.gadget", implements=Widget
):
    """
    A component the sequences can hold
    """


# a component with sequences of components whose defaults name a class
class Box(pyre.component, family="pyre.tests.sequences.anonymous.box"):
    """
    A component with a list and a tuple of components
    """

    # the list
    items = pyre.properties.list(schema=Widget())
    items.default = [Gadget]

    # the tuple
    pair = pyre.properties.tuple(schema=Widget())
    pair.default = (Gadget, Gadget)


def test() -> None:
    """
    Read the sequences of the class and of two instances, then name an entry
    """
    # go through the sequences
    for name in ("items", "pair"):
        # get the entries of the class
        entries = getattr(Box, name)
        # every one is an instance of the class it was handed
        assert all(isinstance(entry, Gadget) for entry in entries)
        # with no name
        assert all(entry.pyre_name is None for entry in entries)

    # make two instances
    one = Box(name="one")
    two = Box(name="two")
    # go through the sequences
    for name in ("items", "pair"):
        # get the entries of the class and of each instance
        mine, first, second = (getattr(box, name) for box in (Box, one, two))
        # each instance has entries of its own
        assert all(isinstance(entry, Gadget) for entry in first + second)
        # with no name
        assert all(entry.pyre_name is None for entry in first + second)
        # which are not those of the class
        assert not {id(entry) for entry in mine} & {id(entry) for entry in first + second}
        # nor those of the other instance
        assert not {id(entry) for entry in first} & {id(entry) for entry in second}
        # and reading them again hands back the same ones
        assert all(a is b for a, b in zip(first, getattr(one, name)))

    # name an entry in the specification
    one.items = ["pyre.tests.sequences.anonymous.widgets.gadget#named"]
    # it is an instance of the class the specification names
    assert isinstance(one.items[0], Gadget)
    # with the name it asked for
    assert one.items[0].pyre_name == "named"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
