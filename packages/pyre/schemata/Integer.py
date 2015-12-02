# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .Numeric import Numeric


# declaration
class Integer(Numeric):
    """
    A type declarator for integers
    """


    # constants
    typename = 'int' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a float
        """
        # for strings
        if isinstance(value, str):
            # strip
            value = value.strip()
            # check for "none"
            if value.lower() == "none":
                # do as told
                return None
            # otherwise, get the interpreter to evaluate simple expressions
            value = eval(value)
        # attempt to
        try:
            # cast {value} into an integer
            return int(value)
        # if that fails
        except (TypeError, ValueError) as error:
            # complain
            raise self.CastingError(value=value, description=str(error)) from None


    # meta-methods
    def __init__(self, default=int(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
