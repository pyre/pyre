# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Type import Type


class Object(Type):
    """
    A generic type declarator
    """


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Convert the given value into a python native object
        """
        return value


# end of file 
