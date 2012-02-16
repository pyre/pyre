# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from . import gsl # the extension


# the class declaration:w

class RNG:
    """
    Encapsulation of the psedu-random number generators in GSL
    """


    # constants
    available = gsl.rng_avail()
    # public data
    algorithm = None

    @property
    def algorithm(self):
        return gsl.rng_name(self.rng)


    # interface


    # meta methods
    def __init__(self, algorithm=None, seed=0, **kwds):
        super().__init__(**kwds)

        # build the RNG
        self.rng = gsl.rng_alloc(algorithm)
        # and seed it
        gsl.rng_set(self.rng, int(seed))

        return


    # private data
    rng = None


# end of file 
