# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Component import Component
from Functor import Functor


class Gaussian(Component, family="gauss.functors.gaussian", implements=Functor):
    """
    An implementation of the normal distribution with mean #@$\mu$@ and variance #@$\sigma^2$@
    """

    # public state
    mean = pyre.components.array()
    mean.doc = "the position of the mean of the Gaussian distribution"
    mean.default = [0.0]

    spread = pyre.components.float()
    spread.doc = "the variance of the Gaussian distribution"
    spread.default = 1.0


    @pyre.components.export
    def eval(self, points):
        """
        Compute the value of the gaussian
        """
        # access the math symbols
        from math import exp, sqrt, pi
        # cache the inventory items
        mean = self.mean
        spread = self.spread
        # precompute the normalization factor
        normalization = 1 / sqrt(2*pi) / spread
        # and the scaling of the exposnential
        scaling = 2 * spread**2
        # loop over points and yield the computed value
        for x in points:
            # compute |x - mean|^2
            # this works as long as x and mean have the same length
            r2 = sum((x_i - mean)**2 for x_i, mean_i in zip(x, mean))
            # yield the value at the xurrent x
            yield normalization * exp(- r2 / scaling)

        return


# end of file 
