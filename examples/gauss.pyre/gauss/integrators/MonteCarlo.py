# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre

# interfaces
from .Integrator import Integrator
from ..shapes.Shape import Shape
from ..functors.Functor import Functor
from ..meshes.PointCloud import PointCloud

# components
from ..shapes.Box import Box
from ..shapes.Ball import Ball
from ..functors.One import One
from ..meshes.Mersenne import Mersenne


class MonteCarlo(pyre.component, family="gauss.integrators.montecarlo", implements=Integrator):
    """
    A Monte Carlo integrator
    """

    # public state
    samples = pyre.properties.int(default=10**5)
    samples.doc = "the number of integrand evaluations"

    box = pyre.facility(interface=Shape, default=Box)
    box.doc = "the bounding box for my mesh"

    mesh = pyre.facility(interface=PointCloud, default=Mersenne)
    mesh.doc = "the generator of points at which to evaluate the integrand"

    region = pyre.facility(interface=Shape, default=Ball)
    region.doc = "the shape that defines the region of integration"

    integrand = pyre.facility(interface=Functor, default=One)
    integrand.doc = "the functor to integrate"


    # interface
    @pyre.export
    def integrate(self):
        """
        Compute the integral as specified by my public state
        """
        # get the set of points
        points = self.mesh.points(count=self.samples, box=self.box)
        # narrow the set down to the ones interior to the region of integration
        interior = self.region.contains(points)
        # sum up and scale the integrand contributions
        integral = self.box.measure()/self.samples * sum(self.integrand.eval(interior))
        # and return the value
        return integral


# end of file 
