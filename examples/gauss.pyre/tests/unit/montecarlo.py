#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the MonteCarlo integrator works as expected
"""


def test():
    import gauss

    from math import pi as π

    # instantiate the integrand
    one = gauss.functors.one("one")

    # instantiate the region of integration
    disk = gauss.shapes.ball("disk")
    disk.origin = (0,0)
    disk.radius = 1.0

    # instantiate the point cloud generator
    mesh = gauss.generators.wickmannhill("mesh")

    # instantiate the integrator
    mc = gauss.integrators.montecarlo(name="mc")
    mc.samples = 10**5
    mc.box = ((0,0), (1,1))
    mc.cloud = mesh
    mc.region = disk
    mc.integrand = one

    # integrate
    integral = mc.integrate()

    # check the answer
    # print("π =", 4*mc.integrate())
    # print("error =", π - 4*integral)
    assert (π - 4*integral) < 1.0e-2

    return mc


# main
if __name__ == "__main__":
    test()


# end of file 
