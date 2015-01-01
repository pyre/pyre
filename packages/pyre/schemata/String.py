# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .Schema import Schema


# declaration
class String(Schema):
    """
    A type declarator for strings
    """


    # constants
    typename = 'str' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a string
        """
        # let the constructor do its job
        return str(value)


    # meta-methods
    def __init__(self, default=str(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
