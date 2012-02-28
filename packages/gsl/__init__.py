# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


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
    from . import gsl
# if this fails
except ImportError:
    # not much to do...
    msg = "could not load the 'gsl' extension module"
    # complain
    import journal
    raise journal.error('gsl').log(msg)


# otherwise, all is well;
# pull in the administrivia
version = gsl.version
copyright = gsl.copyright
def license() : print(gsl.license())


# linear algebra
from .Matrix import Matrix as matrix
from .Vector import Vector as vector

# random numbers
from .RNG import RNG as rng
from . import pdf


# end of file 
