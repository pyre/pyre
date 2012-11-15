# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

class Integrator(pyre.interface, family="gauss.integrators"):
    """
    Interface declarator for integrators
    """

    # access to the required interfaces
    from ..shapes import shape
    from ..functors import functor

    # required public state
    region = pyre.facility(interface=shape)
    region.doc = "the region of integration"

    integrand = pyre.facility(interface=functor)
    integrand.doc = "the functor to integrate"

    # my preferred implementation
    @classmethod
    def default(cls):
        # use {MonteCarlo} by default
        from .MonteCarlo import MonteCarlo
        return MonteCarlo

    # required interface
    @pyre.provides
    def integrate(self):
        """
        Compute the integral of {integrand} over {region}
        """

# end of file 
