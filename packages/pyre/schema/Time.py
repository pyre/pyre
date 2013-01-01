# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Type import Type


class Time(Type):
    """
    A class declarator for timestamp
    """


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a timestamp
        """
        # get the interpreter to evaluate simple expressions
        if isinstance(value, str):
            value = eval(value)
        # attempt to cast {value} into a time object
        raise NotImplementedError("class {.__name__!r} must implement 'cast'".format(cls))


# end of file 
