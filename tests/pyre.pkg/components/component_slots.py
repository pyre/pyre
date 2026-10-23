#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that class and instance trait values interact the way the attributes of python classes
and their instances do
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
    # and another
    g2 = gaussian(name="g2")
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
    # the second still sees the mean of the class
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
    # the second has no values of its own, so it sees the new mean of the class
    assert g2.mean == 2
    # and its new spread
    assert g2.spread == 0.75

    # all done
    return gaussian, g1, g2


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
