# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import collections.abc

# superclass
from .Schema import Schema


# declaration
class Array(Schema):
    """
    The array type declarator
    """

    # constants
    typename = "array"  # the name of my type
    complaint = "could not coerce {0.value!r} to an array"

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a tuple
        """
        # evaluate the string
        if isinstance(value, str):
            # strip it
            value = value.strip()
            # if there is nothing left
            if not value:
                # return an empty tuple
                return ()
            # otherwise, ask python to process
            value = eval(value)
        # if {value} is an iterable
        if isinstance(value, collections.abc.Iterable):
            # convert it to a tuple and return it
            return tuple(value)
        # otherwise flag it as bad input
        raise self.CastingError(value=value, description=self.complaint)

    # meta-methods
    def __init__(self, default=(), **kwds):
        # chain up, potentially with my local default value
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
