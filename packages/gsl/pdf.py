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
    def sample(self):
        """
        Sample the uniform distribution using a random value from {rng}
        """
        # get the value
        return gsl.uniform_sample(self.support, self.rng.rng)


    def density(self, x):
        """
        Compute the probability density of the uniform distribution at {x}
        """
        # get the value
        return gsl.uniform_density(self.support, x)


    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        return gsl.uniform_vector(self.support, self.rng.rng, vector.data)


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        return gsl.uniform_matrix(self.support, self.rng.rng, matrix.data)


    # meta methods
    def __init__(self, support, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
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
    def sample(self):
        """
        Sample the gaussian distribution using a random value from {rng}
        """
        # get the value
        return gsl.gaussian_sample(self.sigma, self.rng.rng)


    def density(self, x):
        """
        Compute the probability density of the gaussian distribution at {x}
        """
        # get the value
        return gsl.gaussian_density(self.sigma, x)


    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        return gsl.gaussian_vector(self.sigma, self.rng.rng, vector.data)


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        return gsl.gaussian_matrix(self.sigma, self.rng.rng, matrix.data)


    # meta methods
    def __init__(self, sigma, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.sigma = sigma
        return


    # implementation details
    sigma = None


# end of file 
