# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Type import Type


# declaration
class Boolean(Type):
    """
    A type declarator for booleans
    """


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Convert {value} into a boolean
        """
        # native type pass through unchanged
        if isinstance(value, bool): return value
        # strings go through the translation map
        if isinstance(value, str): return cls._strmap[value.lower()]
        # anything else is an error
        raise cls.CastingError(description='could not cast {0.value!r} to bool', value=value)


    # strings recognized as booleans
    _strmap = {
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
