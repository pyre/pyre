# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# declaration
class Schema:
    """
    The base class for type declarators
    """


    # exception
    from .exceptions import CastingError

    # constants
    typename = 'identity'


    # public data
    @property
    def default(self):
        """
        Grant access to my default value
        """
        # easy enough
        return self._default

    @default.setter
    def default(self, value):
        """
        Save {value} as my default
        """
        # also easy
        self._default = value
        # all done
        return


    # interface
    def coerce(self, value, **kwds):
        """
        Convert the given value into a python native object
        """
        # just leave it alone
        return value


    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my default value
        self._default = default
        # all done
        return


# end of file
