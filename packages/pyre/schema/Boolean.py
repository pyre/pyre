# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Type import Type


class Boolean(Type):
    """
    A boolean type declarator
    """


    # interface
    @classmethod
    def cast(cls, value):
        """
        Attempt to convert {value} into a boolean
        """
        # native type pass through unchanged
        if isinstance(value, bool):
            return value
        # strings go through the translation map
        if isinstance(value, str):
            return cls._strmap[value.lower()]
        # anything else is an error
        raise cls.CastingError(msg='could not cast to bool', value=value)


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
