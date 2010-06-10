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
    def cast(cls, value, converter=float):
        """
        Attempt to convert {value} into an array using {converter}
        """
        # None means uninitialized
        if value is None:
            return value
        # strings require some lexical analysis
        if value and isinstance(value, str):
            # remove any leading delimiters
            value = value[1:] if value[0] in '[({' else value
            # remove any trailing delimiters
            value = value[:-1] if value[-1] in '])}' else value
            # if this left us with an empty string, return an empty tuple
            if not value: return ()
            # otherwise split it and fall through to the iterable case
            value = value.split(',')
        # if we were handed an iterable, apply {converter} to it and return a tuple
        if isinstance(value, collections.Iterable):
            try:
                return tuple(map(converter, value))
            except TypeError as error:
                raise cls.CastingError(value=value, msg=str(error)) from error
        # otherwise flag it as bad input
        raise cls.CastingError(value=value, msg="unknown type: value={!r}".format(value))


# end of file 
