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
        Convert the given value into my native type
        """
        # obligations...
        raise NotImplementedError("class {.__name__!r} must implement 'coerce'".format(cls))


    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my default value
        self.default = default
        # all done
        return


# end of file 
