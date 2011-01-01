# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Type import Type


class Boolean(Type):
    """
    A type declarator for booleans
    """


    # interface
    @classmethod
    def pyre_cast(cls, value, **kwds):
        """
        Convert {value} into a boolean
        """
        # native type pass through unchanged
        if isinstance(value, bool):
            return value
        # strings go through the translation map
        if isinstance(value, str):
            return cls._strmap[value.lower()]
        # anything else is an error
        raise cls.CastingError(description='could not cast to bool', value=value)


    _strmap = {
        "1": True,
        "y" : True,
        "yes" : True,
        "on" : True,
        "t" : True,
        "true" : True,
        "0": False,
        "n" : False,
        "no" : False,
        "off" : False,
        "f" : False,
        "false" : False,
        }


# end of file 
