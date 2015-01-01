# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access the package with support for rational number
import fractions
# and my superclass
from .Numeric import Numeric


class Fraction(Numeric):
    """
    A type declarator for fixed point numbers
    """


    # constants
    typename = 'fraction' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a fraction
        """
        # let the constructor do its job
        return fractions.Fraction(value)


    # meta-methods
    def __init__(self, default=fractions.Fraction(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
