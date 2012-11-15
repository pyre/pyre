# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
from ..meshes import cloud
from ..functors import functor
from ..shapes import shape, box, ball
from .Integrator import Integrator

class MonteCarlo(pyre.component, family="gauss.integrators.montecarlo",
                 implements=Integrator):
    """
    A Monte Carlo integrator
    """

    # public state
    samples = pyre.properties.int(default=10**5)
    samples.doc = "the number of integrand evaluations"

    box = pyre.facility(interface=shape, default=box)
    box.doc = "the bounding box for my mesh"

    mesh = pyre.facility(interface=cloud)
    mesh.doc = "the generator of points at which to evaluate the integrand"

    region = pyre.facility(interface=shape, default=ball)
    region.doc = "the shape that defines the region of integration"

    integrand = pyre.facility(interface=functor)
    integrand.doc = "the functor to integrate"

    # interface
    @pyre.export
    def integrate(self):
        """
        Compute the integral as specified by my public state
        """
        # compute the overall normalization
        normalization = self.box.measure()/self.samples
        # get the set of points
        points = self.mesh.points(n=self.samples, box=self.box)
        # select the points interior to the region of integration
        interior = self.region.interior(points)
        # sum up and scale the integrand contributions
        integral = normalization * sum(self.integrand.eval(interior))
        # and return the value
        return integral


# end of file 
