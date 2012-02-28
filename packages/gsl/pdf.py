# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
from . import gsl


# the uniform probability distribution
class uniform:
    """
    Encapsulation of the uniform probability distribution
    """


    # interface
    def sample(self, rng):
        """
        Sample the uniform distribution using a random value from {rng}
        """
        # get the value
        return gsl.uniform_sample(self.support, rng.rng)


    def density(self, x):
        """
        Compute the probability density of the uniform distribution at {x}
        """
        # get the value
        return gsl.uniform_density(self.support, x)


    # meta methods
    def __init__(self, support, **kwds):
        super().__init__(**kwds)
        self.support = support
        return


    # implementation details
    support = None


# the gaussian probability distribution
class gaussian:
    """
    Encapsulation of the gaussian probability distribution
    """


    # interface
    def sample(self, rng):
        """
        Sample the gaussian distribution using a random value from {rng}
        """
        # get the value
        return gsl.gaussian_sample(self.sigma, rng.rng)


    def density(self, x):
        """
        Compute the probability density of the gaussian distribution at {x}
        """
        # get the value
        return gsl.gaussian_density(self.sigma, x)


    # meta methods
    def __init__(self, sigma, **kwds):
        super().__init__(**kwds)
        self.sigma = sigma
        return


    # implementation details
    support = None


# end of file 
