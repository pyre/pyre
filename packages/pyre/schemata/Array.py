# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import collections
# superclass
from .Type import Type


# declaration
class Array(Type):
    """
    The array type declarator
    """


    # constants
    typename = 'array' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a tuple
        """
        # evaluate the string
        if isinstance(value, str): value = eval(value)
        # if {value} is an iterable, convert it to a tuple and return it
        if  isinstance(value, collections.Iterable): return tuple(value)
        # otherwise flag it as bad input
        raise self.CastingError(value=value, description="unknown type: value={0.value!r}")


    # meta-methods
    def __init__(self, default=(), **kwds):
        # chain up, potentially with my local default value
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
