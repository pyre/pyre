# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import time
# superclass
from .Type import Type


# my declaration
class Date(Type):
    """
    A type declarator for dates
    """

    # the default format
    format = "%Y-%m-%d"


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a date
        """
        # attempt to 
        try:
           # cast {value} into a date
            return time.strptime(value, self.format)
        # if this fails
        except ValueError as error:
            # complain
            raise self.CastingError(value=value, description=str(error))


    # meta-methods
    def __init__(self, format=format, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file 
