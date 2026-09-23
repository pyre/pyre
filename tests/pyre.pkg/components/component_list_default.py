#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a {list} trait declared with a non-empty default and no schema for its items
can be built: the item schema comes from the trait layer, so the configuration store can ask
it how to evaluate each item
"""

# support
import pyre


# a component with a list that has something in it by default
class Bag(pyre.component, family="containers.list"):
    """
    A bag with a list in it
    """

    names = pyre.properties.list(default=["a", "b"])


def test():
    # build one
    bag = Bag(name="containers.list.default")
    # the default comes through, item by item
    assert list(bag.names) == ["a", "b"]
    # the item schema is a trait, not a bare declarator, and it is the trait counterpart of
    # the schemata default: items pass through as they are
    assert Bag.pyre_trait("names").schema.typename == "identity"

    # values assigned later go through the same item schema
    bag.names = ("c",)
    assert list(bag.names) == ["c"]
    # all done
    return bag


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
