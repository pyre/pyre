# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Type import Type


class Integer(Type):
    """
    A class declarator for integers
    """


    # interface
    @classmethod
    def pyre_cast(cls, value, **kwds):
        """
        Attempt to convert {value} into a float
        """
        # get the interpreter to evaluate simple expressions
        if isinstance(value, str):
            value = eval(value)
        # attempt to cast {value} into an integer
        try:
            return int(value)
        except TypeError as error:
            raise cls.CastingError(value=value, description=str(error)) from error
        except ValueError as error:
            raise cls.CastingError(value=value, description=str(error)) from error


# end of file 
