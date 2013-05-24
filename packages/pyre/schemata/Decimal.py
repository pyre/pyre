# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access the decimal package
import decimal
# and my superclass
from .Type import Type


class Decimal(Type):
    """
    A type declarator for fixed point numbers
    """


    # constants
    typename = 'decimal' # the name of my type
    default = decimal.Decimal() # my default value


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a decimal
        """
        # let the constructor do its job
        return decimal.Decimal(value)


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
