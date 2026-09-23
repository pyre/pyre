#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an {array} trait declared with a non-empty default and no schema for its items
can be built: the item schema comes from the trait layer, so the configuration store can ask
it how to evaluate each item
"""

# support
import pyre


# a component with an array that has something in it by default
class Bag(pyre.component, family="containers.array"):
    """
    A bag with an array in it
    """

    support = pyre.properties.array(default=(0, 1))


def test():
    # build one
    bag = Bag(name="containers.array.default")
    # the default comes through, item by item
    assert tuple(bag.support) == (0.0, 1.0)
    # and the items are floats
    assert all(isinstance(item, float) for item in bag.support)
    # the item schema is a trait, not a bare declarator, and it is the trait counterpart of
    # the schemata default: items are floats
    assert Bag.pyre_trait("support").schema.typename == "float"

    # values assigned later go through the same item schema
    bag.support = ("2", "3.5")
    assert tuple(bag.support) == (2.0, 3.5)
    # all done
    return bag


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
