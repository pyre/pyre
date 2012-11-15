# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre

# declaration
class Integrator(pyre.protocol, family="gauss.integrators"):
    """Abstract specification of integrators"""

    # public state
    region = shape()
    region.doc = "the region of integration"

    integrand = functor()
    integrand.doc = "the functor to integrate"

    mesh = cloud()
    mesh.doc = "the points at which to evaluate the integrand"

    # interface
    @pyre.provides
    def integrate(self):
        """Compute the specified integral"""


# end of file 
