#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that class and instance trait values interact the way a python class and the cached
properties of its instances do: an instance follows its class until it reads a trait, and keeps
what it read
"""

# support
import pyre


# a component with a couple of traits
class gaussian(pyre.component):
    """a representation of a gaussian function"""

    # the mean
    mean = pyre.properties.float(default=0)
    # and the spread
    spread = pyre.properties.float(default=0.25)


def test():
    """
    Change the class defaults and the values of an instance, and check what everybody sees
    """
    # the class holds its defaults
    assert gaussian.mean == 0
    # both of them
    assert gaussian.spread == 0.25
    # change the mean
    gaussian.mean = 1
    # and the spread
    gaussian.spread = 0.5
    # the class holds the new mean
    assert gaussian.mean == 1
    # and the new spread
    assert gaussian.spread == 0.5

    # make a functor
    g1 = gaussian(name="g1")
    # another
    g2 = gaussian(name="g2")
    # and a third one, which won't look at its traits for a while
    g3 = gaussian(name="g3")
    # the first sees the mean of the class
    assert g1.mean == 1
    # and its spread
    assert g1.spread == 0.5
    # and so does the second
    assert g2.mean == 1
    # both of them
    assert g2.spread == 0.5

    # give the first one a mean of its own
    g1.mean = 0
    # and a spread
    g1.spread = 0.25
    # the class keeps its mean
    assert gaussian.mean == 1
    # and its spread
    assert gaussian.spread == 0.5
    # the first functor holds its own mean
    assert g1.mean == 0
    # and its own spread
    assert g1.spread == 0.25
    # the second still holds the mean it read from the class
    assert g2.mean == 1
    # and its spread
    assert g2.spread == 0.5

    # change the class defaults again
    gaussian.mean = 2
    # both of them
    gaussian.spread = 0.75
    # the class holds the new mean
    assert gaussian.mean == 2
    # and the new spread
    assert gaussian.spread == 0.75
    # the first functor keeps its own mean
    assert g1.mean == 0
    # and its own spread
    assert g1.spread == 0.25
    # the second keeps the mean it read before the change, like a python cached property
    assert g2.mean == 1
    # and its spread
    assert g2.spread == 0.5
    # the third never read its traits, so it still follows the class and sees the new mean
    assert g3.mean == 2
    # and its new spread
    assert g3.spread == 0.75

    # all done
    return gaussian, g1, g2, g3


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
