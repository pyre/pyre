# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre

# protocols
from .Integrator import Integrator
from ..functors import functor
from ..meshes import cloud
from ..shapes import shape, box, ball

# declaration
class MonteCarlo(pyre.component, family="gauss.integrators.montecarlo"):
    """A Monte Carlo integrator"""

    # public state
    region = shape(default=ball)
    region.doc = "the region of integration"

    integrand = functor()
    integrand.doc = "the functor to integrate"

    mesh = cloud()
    mesh.doc = "the points at which to evaluate the integrand"

    # interface
    @pyre.export
    def integrate(self):
        """Compute the integral as specified by my public state"""
        # get the set of points
        points = self.mesh.points()
        # narrow the set to the interior of the region of integration
        interior = self.region.contains(points)
        # compute the normalization
        normalization = self.mesh.box.measure()/self.mesh.samples
        # sum up and scale the integrand contributions
        integral = normalization * sum(self.integrand.eval(interior))
        # and return the value
        return integral


# end of file 
