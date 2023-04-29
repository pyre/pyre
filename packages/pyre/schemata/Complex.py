# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import collections.abc

# superclass
from .Number import Number


# declaration
class Complex(Number):
    """
    A type declarator for complex numbers
    """

    # constants
    typename = "complex"  # the name of my type
    complaint = "could not coerce {0.value!r} into a complex number"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a complex number
        """
        # attempt to convert into a complex number
        try:
            # if it is a string
            if isinstance(value, str):
                # get the interpreter to evaluate simple expressions
                value = eval(value, self.context)
            # if it is an iterable
            if isinstance(value, collections.abc.Iterable):
                # unpack it and instantiate it
                return complex(*value)
            # otherwise, just invoke the constructor
            return complex(value)
        # if anything whatsoever goes wrong
        except Exception as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint)

    # meta-methods
    def __init__(self, default=complex(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
