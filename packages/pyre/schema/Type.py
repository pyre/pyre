# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Type:
    """
    The base class for type declarators
    """


    # exception
    from .exceptions import CastingError


    # interface
    @classmethod
    def coerce(cls, *args, **kwds):
        """
        Convert the given value into the native type i represent
        """
        raise NotImplementedError(
            "class {.__name__!r} must implement 'cast'".format(cls))


    # support for building nodes
    @classmethod
    def macro(cls, model):
        """
        Return my preferred macro factory
        """
        # by default, we build expressions
        return model.expression
    

# end of file 
