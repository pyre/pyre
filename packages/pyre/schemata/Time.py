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
class Time(Schema):
    """
    A type declarator for timestamps
    """


    # constants
    format = "%Y-%m-%d %H:%M:%S" # the default format
    typename = 'time' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a timestamp
        """
        # treat false values as uninitialized
        if not value: return None

        # perhaps {value} is already a {datetime} instance
        if isinstance(value, datetime.datetime):
            # in which case just return it
            return value

        # otherwise attempt to
        try:
            # otherwise, assume it is a string; strip
            value = value.strip()
            # check for "none"
            if value.lower() == "none":
                # do as told
                return None
           # cast {value} into a timestamp
            return datetime.datetime.strptime(value, self.format)
        # if this fails
        except (AttributeError, TypeError, ValueError) as error:
            # complain
            raise self.CastingError(value=value, description=str(error))


    # meta-methods
    def __init__(self, default=datetime.datetime.today(), format=format, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file
