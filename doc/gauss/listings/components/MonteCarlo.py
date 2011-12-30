# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

# the interface i implement
from .Integrator import Integrator

# my requirements
from .Shape import Shape
from .Functor import Functor
from .PointCloud import PointCloud


class MonteCarlo(pyre.component, family="gauss.integrators.montecarlo", implements=Integrator):
    """
    Component that implements a Monte Carlo integrator
    """

    # public state
    box = pyre.facility(interface=Shape)
    box.doc = "the bounding box of my cloud of points"

    samples = pyre.properties.int(default=10**5)
    samples.doc = "the number of evaluations of the integrand"

    # my requirements
    region = pyre.facility(interface=Shape)
    region.doc = "the region of integration"
    
    integrand = pyre.facility(interface=Functor)
    integrand.doc = "the functor to integrate"

    mesh = pyre.facility(interface=PointCloud)
    mesh.doc = "the cloud of function evaluation points"

    
    # interface
    @pyre.export
    def integrate(self):
        """
        Compute the integral
        """
        # get the set of points
        points = self.mesh.points(count=self.samples, box=self.box)
        # filter out the ones exterior to the region of integration
        interior = self.region.contains(points)
        # sum up the integrand contributions at those points and return the integral
        integral = self.box.measure() / self.samples * sum(self.integrand.eval(interior))
        # and return the value
        return integral


# end of file 
