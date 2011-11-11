# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre


class Integrator(pyre.interface, family="gauss.integrators"):
    """
    Interface declarator for integrators
    """


    # access to the required interfaces
    from ..shapes.Shape import Shape
    from ..functors.Functor import Functor

    # public state
    region = pyre.facility(interface=Shape)
    region.doc = "the region of integration"

    integrand = pyre.facility(interface=Functor)
    integrand.doc = "the functor to integrate"


    # interface
    @pyre.provides
    def integrate(self):
        """
        Compute the integral of {integrand} over {region}
        """


# end of file 
