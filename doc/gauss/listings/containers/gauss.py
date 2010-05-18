#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


def gauss():
    from Disk import Disk
    from MersenneTwister import MersenneTwister

    # initialize the counters
    total = 10**5
    interior = 0
    # the bounding box
    box = [(0,0), (1,1)]
    # the point cloud generator
    generator = MersenneTwister()
    # the region of integration
    disk = Disk(center=(0,0), radius=1)

    # the integration algorithm
    # build the point sample
    sample = generator.points(total, box)
    # count the interior points
    for flag in disk.interior(sample):
        if flag is True:
            interior += 1

    # print out the estimate of π
    print("pi: {0:.8f}".format(4*interior/total))
    return


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
    
    print(sum(disk.contains(points)))

    return


# main
if __name__ == "__main__":
    gauss()

# end of file 
