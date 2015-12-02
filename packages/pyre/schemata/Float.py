# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .Numeric import Numeric


# declaration
class Float(Numeric):
    """
    A type declarator for floats
    """


    # constants
    typename = 'float' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a float
        """
        # if it is a string
        if isinstance(value, str):
            # check for none
            if value.strip().lower() == "none":
                # and do as told
                return None
            # otherwise, get the interpreter to evaluate simple expressions
            value = eval(value)
        # attempt to
        try:
            # cast {value} into a float
            return float(value)
        # if it didn't work
        except (TypeError, ValueError) as error:
            # complain
            raise self.CastingError(value=value, description=str(error)) from None


    # meta-methods
    def __init__(self, default=float(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
