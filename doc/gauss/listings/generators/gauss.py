#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


def gauss():
    """
    The driver for the generator based implementation
    """
    from Disk import Disk
    from MersenneTwister import MersenneTwister

    # inputs
    N = 10**5
    box = [(0,0), (1,1)]
    # the point cloud generator
    generator = MersenneTwister()
    # the region of integration
    disk = Disk(center=(0,0), radius=1)

    # the integration algorithm
    # build the point sample
    sample = generator.points(N, box)
    # count the interior points
    interior = count(disk.interior(sample))

    # print out the estimate of #@$\pi$@
    print("pi: {0:.8f}".format(4*interior/N))
    return


def count(iterable): #@\label{line:driver:generators:count}@
    """
    Count the entries of iterable
    """
    counter = 0
    for item in iterable:
        counter += 1
    return counter


def testMT():
    from MersenneTwister import MersenneTwister
    wh = MersenneTwister()

    sample = wh.generateSample(2, [(0, 1),(1, 2)])

    print(sample)

    return


def testDisk():
    from Disk import Disk
    disk = Disk(center=(0,0), radius=1)

    points = [
        (0, 0),
        (.5, .5),
        (1, 1)
        ]
    
    print(count(disk.contains(points)))

    return


# main
if __name__ == "__main__":
    gauss()

# end of file 
