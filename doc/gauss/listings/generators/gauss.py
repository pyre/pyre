#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


def gauss():
    from Disk import Disk
    from WichmannHill import WichmannHill

    # inputs
    total = 10**5
    box = [(0,0), (1,1)]
    # the point cloud generator
    generator = WichmannHill()
    # the region of integration
    disk = Disk(center=(0,0), radius=1)

    # the integration algorithm
    sample = generator.points(total, box)
    interior = sum(disk.interior(sample))

    # print out the estimate of π
    print("pi: {0:.8f}".format(4*interior/total))

    return


def testWH():
    from WichmannHill import WichmannHill
    wh = WichmannHill()

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
