#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import operator, functools

def gauss():
    """
    The driver for the generator based implementation
    """
    from Disk import Disk
    from Gaussian import Gaussian
    from MersenneTwister import MersenneTwister

    # inputs
    N = 10**7
    box = [(-1,-1), (1,1)]
    B = functools.reduce(operator.mul, ((right-left) for left,right in zip(*box)))#@\label{line:mc:volume}@
    # the point cloud generator
    generator = MersenneTwister()
    # the region of integration
    disk = Disk(center=(0,0), radius=1)
    # the integrand
    gaussian = Gaussian(mean=(0,0), spread=1/3)

    # the integration algorithm
    # build the point sample
    sample = generator.points(N, box)
    # select the interior points
    interior = disk.interior(sample)
    # compute the integral
    integral = B/N * sum(gaussian.eval(interior))#@\label{line:mc:integral}@

    # print out the estimate of the integral
    print("integral: {0:.8f}".format(integral))
    return


# main
if __name__ == "__main__":
    gauss()

# end of file 
