#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# get the metaclass
# MGA - 20201223: for some strange and suspicious reason, the {import} must outside
#     {create_instances}, otherwise the instances are not properly garbage collected. this
#     makes little sense at this point, and is not the case for {p2}
from pyre.patterns.Extent import Extent


# declare and instantiate a small class hierarchy
def create_instances():
    """
    Verify that extent aware classes track their instances correctly
    """
    # make an extent aware class
    class Base(metaclass=Extent):
        """
        An extent aware base class
        """

    class Derived(Base):
        """
        A derived class whose extent is counted by {Base}
        """

    class Root(Derived, pyre_extent=True):
        """
        Another derived class that wants to track its extent on its own
        """

    class Leaf(Root):
        """
        A {Root} subclass whose extent is counted by {Root}
        """

    # make some instances
    b1 = Base()
    b2 = Base()

    d1 = Derived()
    d2 = Derived()

    r1 = Root()
    r2 = Root()

    l1 = Leaf()
    l2 = Leaf()

    # verify the extents
    assert set(Base.pyre_extent) == { b1, b2, d1, d2 }
    assert set(Root.pyre_extent) == { r1, r2, l1, l2 }

    # all done
    return Base, Derived, Root, Leaf


def test():
    """
    Make some instances, verify that the extent is computed correctly, and then verify that it
    is empty after all instances gave been destructed
    """
    # run the test with actual instances
    Base, Derived, Root, Leaf = create_instances()

    # now that these instances have been garbage collected, verify that the extents are empty
    assert set(Base.pyre_extent) == set()
    assert set(Root.pyre_extent) == set()

    # verify the structural invariants
    # {Base} and {Derived} share
    assert Base.pyre_extent is Derived.pyre_extent
    # {Root} and {Leaf} share
    assert Root.pyre_extent is Leaf.pyre_extent
    # {Base} and {Root} do not
    assert Base.pyre_extent is not Root.pyre_extent

    # all done
    return Base, Derived, Root, Leaf


# main
if __name__ =="__main__":
    # run the test
    test()


# end of file
