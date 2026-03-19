# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2026 all rights reserved
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
        return gsl.uniform_sample(self.rng.rng, self.support)


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
        gsl.uniform_vector(vector.data, self.rng.rng, self.support)
        # and return it
        return vector


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.uniform_matrix(matrix.data, self.rng.rng, self.support)
        # and return it
        return matrix


    # meta methods
    def __init__(self, support=(0, 1), rng=None, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.support = support
        return


    # implementation details
    support = (0, 1)


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
        return gsl.uniform_pos_sample(self.rng.rng, self.support)


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
        gsl.uniform_pos_vector(vector.data, self.rng.rng, self.support)
        # and return it
        return vector


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.uniform_pos_matrix(matrix.data, self.rng.rng, self.support)
        # and return it
        return matrix


    # meta methods
    def __init__(self, support=(0, 1), rng=None, **kwds):
        super().__init__(**kwds)
        self.support = support
        self.rng = rng
        return


    # implementation details
    support = (0, 1)


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
        return gsl.gaussian_sample(self.rng.rng, self.mean, self.sigma)


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
        gsl.gaussian_vector(vector.data, self.rng.rng, self.mean, self.sigma)
        # and return it
        return vector


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.gaussian_matrix(matrix.data, self.rng.rng, self.mean, self.sigma)
        # and return it
        return matrix


    # meta methods
    def __init__(self, mean=0.0, sigma=1.0, rng=None, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.mean = mean
        self.sigma = sigma
        return


    # implementation details
    mean = 0.0
    sigma = 1.0


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
        return gsl.ugaussian_sample(self.rng.rng, self.mean)


    def density(self, x):
        """
        Compute the probability density of the gaussian distribution at {x}
        """
        # get the value
        return gsl.ugaussian_density(self.mean, x)


    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # fill the vector
        gsl.ugaussian_vector(vector.data, self.rng.rng, self.mean)
        # and return it
        return vector


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.ugaussian_matrix(matrix.data, self.rng.rng, self.mean)
        # and return it
        return matrix


    # meta methods
    def __init__(self, mean=0.0, rng=None, **kwds):
        super().__init__(**kwds)
        self.mean = mean
        self.rng = rng
        return


    # implementation details
    mean = 0.0


# the truncated gaussian probability distribution
class tgaussian:
    """
    Encapsulation of the truncated gaussian distribution on [a, b]
    PDF(x) = gaussian_pdf(x) / (CDF(b) - CDF(a))
    Sampling via inverse-CDF method
    """


    # interface
    def sample(self):
        """
        Return a sample from the truncated gaussian on [a, b]
        """
        return gsl.tgaussian_sample(self.rng.rng, self.mean, self.sigma, self.support)


    def density(self, x):
        """
        Evaluate the truncated gaussian pdf at {x}
        """
        return gsl.tgaussian_density(self.mean, self.sigma, self.support, x)


    # higher level support
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        gsl.tgaussian_vector(vector.data, self.rng.rng, self.mean, self.sigma, self.support)
        return vector


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        gsl.tgaussian_matrix(matrix.data, self.rng.rng, self.mean, self.sigma, self.support)
        return matrix


    # meta methods
    def __init__(self, support=(-1, 1), mean=0.0, sigma=1.0, rng=None, **kwds):
        super().__init__(**kwds)
        self.support = support
        self.mean = mean
        self.sigma = sigma
        self.rng = rng
        return


    # implementation details
    support = (-1, 1)
    mean = 0.0
    sigma = 1.0


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
        gsl.dirichlet_vector(vector.data, self.rng.rng, self.alpha.data)
        # and return it
        return vector


    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # fill the matrix
        gsl.dirichlet_matrix(matrix.data, self.rng.rng, self.alpha.data)
        # and return it
        return matrix


    # meta methods
    def __init__(self, alpha, rng, **kwds):
        super().__init__(**kwds)
        self.rng = rng
        self.alpha = alpha
        return


# end of file
