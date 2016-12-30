# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access the decimal package
import decimal
# and my superclass
from .Numeric import Numeric


class Decimal(Numeric):
    """
    A type declarator for fixed point numbers
    """


    # constants
    typename = 'decimal' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a decimal
        """
        # check for "none"
        if isinstance(value, str) and value.strip().lower() == "none":
            # do as told
            return None
        # let the constructor do its job
        return decimal.Decimal(value)


    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)


    # meta-methods
    def __init__(self, default=decimal.Decimal(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
