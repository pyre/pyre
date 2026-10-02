# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# interface
def zero(entity):
    """
    Zero out the content of {entity}
    """
    return entity.zero()


def fill(entity, value):
    """
    Set all entries in {entity} to {value}
    """
    return entity.fill(value)


# attempt to
try:
    # load the extension module
    from . import libgsl as gsl
# treat any import failure as the absence of gsl, as {mpi} does: installations that cannot
# build the bindings, e.g. the pip wheels, still ship this package
except ImportError:
    # indicate that there is no runtime support
    gsl = None

    # and that none of the entities the bindings publish are available
    version = None
    copyright = None
    license = None
    histogram = None
    matrix = None
    permutation = None
    rng = None
    vector = None
    Transpose = None
    Triangle = None
    Diagonal = None
    Side = None
    EigenOrder = None
    blas = None
    pdf = None
    linalg = None
    stats = None
# otherwise, we have bindings and hence GSL support
else:
    # get the framework
    import pyre

    # register the package
    package = pyre.executive.registerPackage(name="gsl", file=__file__)
    # record the layout
    home, prefix, defaults = package.layout()

    # pull in the administrivia
    version = gsl.version
    copyright = gsl.copyright

    def license():
        """
        Print the license of the GSL bindings
        """
        # show it
        print(gsl.license())
        # all done
        return

    # wrappers
    from .Histogram import Histogram as histogram
    from .Matrix import Matrix as matrix
    from .Permutation import Permutation as permutation
    from .RNG import RNG as rng
    from .Vector import Vector as vector

    # the blas and eigen flag enumerations, straight from the extension
    Transpose = gsl.Transpose
    Triangle = gsl.Triangle
    Diagonal = gsl.Diagonal
    Side = gsl.Side
    EigenOrder = gsl.EigenOrder

    # other interfaces
    from . import blas, pdf, linalg, stats


# end of file
