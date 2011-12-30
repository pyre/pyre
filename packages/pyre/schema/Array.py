# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import collections
from .Type import Type


class Array(Type):
    """
    The array type declarator
    """


    # interface
    @classmethod
    def pyre_cast(cls, value, **kwds):
        """
        Convert {value} into a tuple
        """
        # evaluate the string
        if isinstance(value, str):
            value = eval(value)
        # if {value} is an iterable, convert it to a  tuple and return it
        if  isinstance(value, collections.Iterable):
            return tuple(value)
        # otherwise flag it as bad input
        raise cls.CastingError(value=value, description="unknown type: value={!r}".format(value))


# end of file 
