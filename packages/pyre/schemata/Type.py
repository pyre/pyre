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
        # chain up
        super().__init__(**kwds)
        # save my default value
        self.default = default
        # all done
        return


# end of file 
