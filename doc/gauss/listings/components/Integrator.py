# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

# my requirements
from .Shape import Shape
from .Functor import Functor

class Integrator(pyre.interface):

    """
    Interface declaration for integrators
    """

    # public state
    region = pyre.components.facility(interface=Shape)
    region.doc = "the region of integration"
    
    integrand = pyre.components.facility(interface=Functor)
    integrand.doc = "the functor to integrate"
    
    # interface
    @pyre.provides
    def integrate(self):
        """
        Compute the integral of the {intergrand} over the {region}
        """


# end of file 
