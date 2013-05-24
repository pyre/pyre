# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Type import Type


# declaration
class String(Type):
    """
    A type declarator for strings
    """


    # constants
    typename = 'str' # the name of my type
    default = str() # my default value


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a string
        """
        # let the constructor do its job
        return str(value)


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
