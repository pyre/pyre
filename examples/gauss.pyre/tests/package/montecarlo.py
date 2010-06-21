#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Compute an estimate for π using the montecarlo integrator as configured entirely from an input
file
"""


def test():
    # access the executive
    import pyre
    executive = pyre.executive()
    # load the local configuration file
    executive.loadConfiguration(uri="vfs:///local/pi.pml")
    # instantiate the integrator
    import gauss
    mc = gauss.integrators.montecarlo(name="mc")

    # print out the configuration state
    executive.calculator._dump(pattern="mc")

    # print out the integrator configuration
    print("mc:")
    print("    samples: {!r}".format(mc.samples))
    print("    box: {!r}".format(mc.box))
    print("    mesh: {!r}".format(mc.mesh))
    print("    region: {!r}".format(mc.region))
    print("    integrand: {!r}".format(mc.integrand))

    # check that it got configured as expected
    # the sample size
    assert mc.samples == 1e6
    # gain access to all the component declarations
    from gauss.shapes.Box import Box
    # verify that the various components have be set to instances of the right types
    assert isinstance(mc.box, Box)


    return
    # integrate
    integral = mc.integrate()

    # check the answer
    # print("π =", 4*integral)
    # print("error =", π - 4*integral)
    assert (π - 4*integral) < 1.0e-2

    return mc


# main
if __name__ == "__main__":
    test()


# end of file 
