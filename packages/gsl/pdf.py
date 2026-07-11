# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from . import libgsl as gsl


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
        return gsl.uniform_sample(self.support, self.rng)

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
        gsl.uniform_vector(self.support, self.rng, vector)
        # and return it
        return vector

    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.uniform_matrix(self.support, self.rng, matrix)
        # and return it
        return matrix

    # meta methods
    def __init__(self, support, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.support = support
        return

    # implementation details
    support = None


# the uniform probability distribution for strictly positive argument
class uniform_pos:
    """
    Encapsulation of the positive uniform probability distribution
    """

    # interface
    def sample(self):
        """
        Sample the uniform distribution using a random value from {rng}
        """
        # get the value
        return gsl.uniform_pos_sample(self.rng)

    def density(self, x):
        """
        Compute the probability density of the uniform distribution at {x}
        """
        # get the value
        return 1.0

    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        gsl.uniform_pos_vector(self.rng, vector)
        # and return it
        return vector

    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.uniform_pos_matrix(self.rng, matrix)
        # and return it
        return matrix

    # meta methods
    def __init__(self, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        return


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
        return gsl.gaussian_sample(self.mean, self.sigma, self.rng)

    def density(self, x):
        """
        Compute the probability density of the gaussian distribution at {x}
        """
        # get the value
        return gsl.gaussian_density(self.mean, self.sigma, x)

    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        gsl.gaussian_vector(self.mean, self.sigma, self.rng, vector)
        # and return it
        return vector

    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.gaussian_matrix(self.mean, self.sigma, self.rng, matrix)
        # and return it
        return matrix

    # meta methods
    def __init__(self, mean, sigma, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.mean = mean
        self.sigma = sigma
        return

    # implementation details
    mean = 0.0
    sigma = None


# the unit gaussian probability distribution
class ugaussian:
    """
    Encapsulation of the unit gaussian probability distribution
    """

    # interface
    def sample(self):
        """
        Sample the gaussian distribution using a random value from {rng}
        """
        # get the value
        return gsl.ugaussian_sample(self.rng)

    def density(self, x):
        """
        Compute the probability density of the gaussian distribution at {x}
        """
        # get the value
        return gsl.ugaussian_density(x)

    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        gsl.ugaussian_vector(self.rng, vector)
        # and return it
        return vector

    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.ugaussian_matrix(self.rng, matrix)
        # and return it
        return matrix

    # meta methods
    def __init__(self, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        return


# the truncated gaussian probability distribution
class tgaussian:
    """
    Encapsulation of the gaussian probability distribution truncated to a finite interval
    """

    # interface
    def sample(self):
        """
        Sample the truncated gaussian using a random value from {rng}
        """
        # get the value
        return gsl.tgaussian_sample(self.mean, self.sigma, self.support, self.rng)

    def density(self, x):
        """
        Compute the probability density of the truncated gaussian at {x}
        """
        # get the value
        return gsl.tgaussian_density(self.mean, self.sigma, self.support, x)

    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        gsl.tgaussian_vector(self.mean, self.sigma, self.support, self.rng, vector)
        # and return it
        return vector

    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.tgaussian_matrix(self.mean, self.sigma, self.support, self.rng, matrix)
        # and return it
        return matrix

    # meta methods
    def __init__(self, mean, sigma, support, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.mean = mean
        self.sigma = sigma
        self.support = support
        return

    # implementation details
    mean = 0.0
    sigma = None
    support = None


# the dirichlet probability distribution
class dirichlet:
    """
    Encapsulation of the dirichlet probability distribution
    """

    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        gsl.dirichlet_vector(self.rng, self.alpha, vector)
        # and return it
        return vector

    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.dirichlet_matrix(self.rng, self.alpha, matrix)
        # and return it
        return matrix

    # meta methods
    def __init__(self, alpha, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.alpha = alpha
        return


# end of file
