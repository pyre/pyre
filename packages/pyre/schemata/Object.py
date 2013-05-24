# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Type import Type


# declaration
class Object(Type):
    """
    A generic type declarator
    """


    # constants
    default = object()
    typename = 'identity'


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Convert the given value into a python native object
        """
        # just leave it alone
        return value


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
