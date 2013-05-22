# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Type import Type


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
        return str(value)


    # support for building nodes
    @classmethod
    def macro(cls, model):
        """
        Return my preferred macro factory
        """
        # by default, i build interpolations
        return model.interpolation
    

# end of file 
