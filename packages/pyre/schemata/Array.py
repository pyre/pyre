# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Sequence import Sequence

# default schema
from .Float import Float


# declaration
class Array(Sequence):
    """
    The array type declarator
    """

    # constants
    typename = "array"  # the name of my type
    complaint = "could not coerce {0.value!r} to an array"

    # meta-methods
    def __init__(self, shape=None, schema=Float(), **kwds):
        # chain up, potentially with my local default value
        super().__init__(schema=schema, **kwds)
        # save my shape
        self.shape = shape
        # all done
        return

    # implementation details
    def _coerce(self, value, incognito=True, **kwds):
        """
        Convert {value} into an iterable
        """
        # evaluate the string
        if isinstance(value, str):
            # strip it
            value = value.strip()
            # if there is nothing left
            if not value:
                # return an empty tuple
                return
            # otherwise, ask python to process
            value = eval(value)
        # delegate to my superclass to build my container
        yield from super()._coerce(value=value, incognito=incognito, **kwds)
        # all done
        return


# end of file
