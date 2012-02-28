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


# end of file 
