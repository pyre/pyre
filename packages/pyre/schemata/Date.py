# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import time
# superclass
from .Schema import Schema


# my declaration
class Date(Schema):
    """
    A type declarator for dates
    """


    # constants
    format = "%Y-%m-%d" # the default date format
    typename = 'date' # the name of my type


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
    def __init__(self, default=time.localtime(), format=format, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file 
