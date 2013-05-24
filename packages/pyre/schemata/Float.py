# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Type import Type


# declaration
class Float(Type):
    """
    A type declarator for floats
    """


    # constants
    typename = 'float' # the name of my type
    default = float() # my default value


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a float
        """
        # get the interpreter to evaluate simple expressions
        if isinstance(value, str): value = eval(value)

        # attempt to 
        try:
            # cast {value} into a float
            return float(value)
        # if it didn't work
        except (TypeError, ValueError) as error:
            # complain
            raise cls.CastingError(value=value, description=str(error)) from None


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
