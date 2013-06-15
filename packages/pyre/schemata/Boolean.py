# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# superclass
from .Type import Type


# declaration
class Boolean(Type):
    """
    A type declarator for booleans
    """


    # constants
    typename = 'bool' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a boolean
        """
        # native type pass through unchanged
        if isinstance(value, bool): return value
        # strings go through the translation map
        if isinstance(value, str): return self.xlat[value.lower()]
        # anything else is an error
        raise self.CastingError(description='could not cast {0.value!r} to bool', value=value)


    # meta-methods
    def __init__(self, default=True, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


    # implementation details
    # strings recognized as booleans
    xlat = {
        '1': True,
        'y' : True,
        'yes' : True,
        'on' : True,
        't' : True,
        'true' : True,
        '0': False,
        'n' : False,
        'no' : False,
        'off' : False,
        'f' : False,
        'false' : False,
        '': True, # mere presence is considered true
        }


# end of file 
