# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Type import Type


class Object(Type):
    """
    A generic type declarator
    """


    # interface
    @classmethod
    def pyre_cast(cls, value, **kwds):
        """
        Convert the given value into a python native object
        """
        return value


# end of file 
