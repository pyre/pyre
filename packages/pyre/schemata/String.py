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


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a string
        """
        # let the constructor do its job
        return str(value)


# end of file 
