# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre

# my ancestor
from pyre.components.Component import Component

# the interface i implement
from ..interfaces.Integrator import Integrator

# my requirements
from ..interfaces.Shape import Shape
from ..interfaces.Functor import Functor
from ..interfaces.PointCloud import PointCloud


class MonteCarlo(Component, family="gauss.integrators.montecarlo", implements=Integrator):
    """
    Component that implements a Monte Carlo integrator
    """

    # public state
    box = pyre.components.facility(interface=Shape)
    box.doc = "the bounding box of my cloud of points"

    samples = pyre.components.int()
    samples.doc = "the number of evaluations of the integrand"
    samples.default = 10**3

    # my requirements
    region = pyre.components.facility(interface=Shape)
    region.doc = "the region of integration"
    
    integrand = pyre.components.facility(interface=Functor)
    integrand.doc = "the functor to integrate"

    mesh = pyre.components.facility(interface=PointCloud)
    mesh.doc = "the cloud of function evaluation points"

    
    # interface
    @pyre.components.export
    def integrate(self):
        """
        Compute the integral
        """
        # get the set of points
        points = self.mesh.points(count=self.samples, box=self.box)
        # filter out the ones exterior to the region of integration
        interior = self.region.contains(points)
        # sum up the integrand contributions at those points and return the integral
        return self.box.measure() / self.samples * sum(self.integrand.eval(interior))


# end of file 
