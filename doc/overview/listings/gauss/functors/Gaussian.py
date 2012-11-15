# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre
from .Functor import Functor

class Gaussian(pyre.component, family="gauss.functor.gaussian",
               implements=Functor):
    """
    An implementation of the normal distribution with
    mean #@$\mu$@ and variance #@$\sigma^2$@
    """

    # public state
    mean = pyre.properties.array(default=[0])
    mean.doc = "the mean of the gaussian distribution"
    mean.aliases.add("#@$\mu$@")

    spread = pyre.properties.float(default=1)
    spread.doc = "the variance of the gaussian distribution"
    spread.aliases.add("#@$\sigma$@")


    # interface
    @pyre.export
    def eval(self, points):
        """
        Compute the value of the gaussian
        """
        # access the math symbols
        from math import exp, sqrt, pi
        # cache the shape information
        mean = self.mean
        spread = self.spread
        # precompute the normalization factor and the exponent scaling
        normalization = 1 / sqrt(2*pi) / spread
        scaling = 2 * spread**2
        # loop over points and yield the computed value
        for p in points:
            # compute the norm |p - mean|^2
            # this works as long as {p} and {mean} have the same length
            r2 = sum((p_i - mean_i)**2 for p_i, mean_i in zip(p, mean))
            # yield the value at the current p
            yield normalization * exp(- r2/scaling)
        # all done    
        return


# end of file 
