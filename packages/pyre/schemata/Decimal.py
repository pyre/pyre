# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# access the decimal package
import decimal

# and my superclass
from .Number import Number


class Decimal(Number):
    """
    A type declarator for fixed point numbers
    """

    # constants
    typename = "decimal"  # the name of my type

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a decimal
        """
        # attempt to
        try:
            # let the constructor do its job
            return decimal.Decimal(value)
        # if anything goes wrong
        except decimal.InvalidOperation as error:
            # convert it into a configuration error
            raise self.CastingError(value=value, description=str(error))

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
