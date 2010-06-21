# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
from .Type import Type


class Array(Type):
    """
    An array type declarator
    """


    # interface
    @classmethod
    def cast(cls, value):
        """
        Attempt to convert {value} into an array using {converter}
        """
        # strings require some lexical analysis
        if value and isinstance(value, str):
            value = eval(value)
        # if value is an iterable, retrun it
        if isinstance(value, collections.Iterable):
            return tuple(value)
        # otherwise flag it as bad input
        raise cls.CastingError(value=value, msg="unknown type: value={!r}".format(value))


# end of file 
