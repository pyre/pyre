# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from . import libgsl as gsl  # the extension


# the class declaration
class RNG(gsl.RNG):
    """
    A pseudo-random number generator

    The generator itself -- its allocation, its algorithms, drawing from it -- is the
    extension's; this subclass supplies the default algorithm and the catalogue of the ones gsl
    was built with
    """

    # the names of the generators gsl knows about
    available = gsl.rng_avail()

    # meta methods
    def __init__(self, algorithm="ranlxs2", **kwds):
        # let the extension build the generator; the algorithm is its to consume
        super().__init__(algorithm=algorithm, **kwds)
        # all done
        return


# end of file
