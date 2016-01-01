# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import datetime
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
        # treat false values as uninitialized
        if not value: return None

        # check whether {value} is already a {date} instance
        if isinstance(value, datetime.date):
            # in which case we are done
            return value
        # perhaps it is a {datetime} instance
        if isinstance(value, datetime.datetime):
            # in which case extract its date component
            return value.date()

        # otherwise, and attempt to
        try:
            # otherwise, assume it is a string; strip
            value = value.strip()
            # check for "none"
            if value.lower() == "none":
                # do as told
                return None
           # cast {value} into a date
            return datetime.datetime.strptime(value, self.format).date()
        # if this fails
        except (AttributeError, TypeError, ValueError) as error:
            # complain
            raise self.CastingError(value=value, description=str(error))


    # meta-methods
    def __init__(self, default=datetime.date.today(), format=format, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file
