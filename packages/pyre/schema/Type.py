# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Type(object):
    """
    The base class for type representations
    """


    # interface
    @classmethod
    def cast(self, **kwds):
        """
        Convert the given value into the native type i represent
        """
        raise NotImplementedError(
            "class {.__name__!r} must implement 'cast'".format(cls))
    

# end of file 
