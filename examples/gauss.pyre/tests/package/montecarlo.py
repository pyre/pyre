#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Configure and integrator entirely from a configuration file and carry out the integration
"""


def test():
    # access the executive
    import pyre
    executive = pyre.executive()
    # load the local configuration file
    executive.loadConfiguration(uri="vfs:///local/pi.pml")
    # print out the configuration state before the class is instantiated
    # executive.calculator._dump(pattern="mc")
    # executive.calculator._dump(pattern="gauss.shapes.box#mc.box")
    # instantiate the integrator
    import gauss
    mc = gauss.integrators.montecarlo(name="mc")
    # print out the configuration state after the class is instantiated
    # executive.calculator._dump(pattern="mc")
    # print out the integrator configuration
    # print("mc:")
    # print("    samples: {!r}".format(mc.samples))
    # print("    box: {!r}".format(mc.box))
    # print("    integrand: {!r}".format(mc.integrand))
    # print("    mesh: {!r}".format(mc.mesh))
    # print("    region: {!r}".format(mc.region))

    # check that it got configured as expected
    # the sample size
    assert mc.samples == 1e5
    # gain access to all the component declarations
    from gauss.functors.Gaussian import Gaussian
    from gauss.meshes.MersenneTwister import MersenneTwister
    from gauss.shapes.Ball import Ball
    from gauss.shapes.Box import Box
    # verify that the various components have been set to instances of the right types
    assert isinstance(mc.box, Box)
    assert isinstance(mc.integrand, Gaussian)
    assert isinstance(mc.mesh, MersenneTwister)
    assert isinstance(mc.region, Ball)
    # and that their values are what we expect
    assert mc.box.diagonal == ((-1,-1), (1,1))
    assert mc.integrand.μ == (0,0)
    assert mc.integrand.σ == 1/3
    assert mc.region.center == (0,0)
    assert mc.region.radius == 1

    # now, integrte
    assert abs(mc.integrate() - .826261) < 1.0e-2

    return mc


# main
if __name__ == "__main__":
    test()


# end of file 
