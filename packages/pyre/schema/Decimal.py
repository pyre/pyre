# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Type import Type


class Decimal(Type):
    """
    A class declarator for fixed point numbers
    """


    # interface
    @classmethod
    def pyre_cast(cls, value, **kwds):
        """
        Attempt to convert {value} into a decimal
        """
        # get the interpreter to evaluate simple expressions
        if isinstance(value, str):
            value = eval(value)
        # attempt to cast {value} into a decimal
        raise NotImplementedError("class {.__name__!r} must implement 'cast'".format(cls))


# end of file 
