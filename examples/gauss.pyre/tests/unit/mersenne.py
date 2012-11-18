#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the MersenneTwister generator behaves as expected
"""


def test():
    import gauss

    # instantiate
    mt = gauss.meshes.mersenne(name="mt")
    # the number of points to generate
    size = 5
    # specify the box
    box = gauss.shapes.box(name="box")
    box.intervals = ((0,1), (0,1))
    # make a bunch of random points
    points = tuple(mt.points(box=box, count=size))
    # check the length
    assert len(points) == size
    # verify they all lie inside the box
    intervals = tuple(box.intervals)
    for point in points:
        for p, (left,right) in zip(point, intervals):
            assert p>=left and p<=right

    return box


# main
if __name__ == "__main__":
    test()


# end of file 
