# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Interface import Interface

# my requirements
from .Shape import Shape
from .Functor import Functor

class Integrator(Interface):

    """
    Interface declaration for integrators
    """

    # public state
    region = pyre.components.facility(interface=Shape)
    region.doc = "the region of integration"
    
    integrand = pyre.components.facility(interface=Functor)
    integrand.doc = "the functor to integrate"
    
    # interface
    @pyre.components.provides
    def integrate(self):
        """
        Compute the integral of the {intergrand} over the {region}
        """


# end of file 
