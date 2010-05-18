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

    # inputs
    N = 10**5
    box = [(0,0), (1,1)]
    # the point cloud generator
    cloud = MersenneTwister()
    # the region of integration
    disk = Disk(center=(0,0), radius=1)

    # the integration algorithm
    total = 0
    interior = 0
    while total < N:
        point = cloud.point(box)
        if disk.interior(point):
            interior += 1
        total += 1

    # print out the estimate of #@$\pi$@
    print("pi: {0:.8f}".format(4*interior/total))
    return


# main
if __name__ == "__main__":
    gauss()

# end of file 
