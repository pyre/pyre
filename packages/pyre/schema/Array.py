# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


import collections
from .Type import Type


class Array(Type):
    """
    The array type declarator
    """


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Convert {value} into a tuple
        """
        # evaluate the string
        if isinstance(value, str):
            value = eval(value)
        # if {value} is an iterable, convert it to a tuple and return it
        if  isinstance(value, collections.Iterable):
            return tuple(value)
        # otherwise flag it as bad input
        raise cls.CastingError(value=value, description="unknown type: value={0.value!r}")


# end of file 
