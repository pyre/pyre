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


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a decimal
        """
        # let the constructor do its job
        return decimal.Decimal(value)


# end of file 
