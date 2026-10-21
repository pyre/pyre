# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
    format = "%Y-%m-%d"  # the default date format
    typename = "date"  # the name of my type
    complaint = "could not coerce {0.value!r} into a date"  # the error message

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a date
        """
        # perhaps it is a {datetime} instance; check it first, since a {datetime} is also a
        # {date}
        if isinstance(value, datetime.datetime):
            # in which case extract its date component
            return value.date()
        # check whether {value} is already a {date} instance
        if isinstance(value, datetime.date):
            # in which case we are done
            return value
        # text
        if isinstance(value, str):
            # strip it
            value = value.strip()
            # if there is nothing left
            if not value:
                # it is uninitialized
                return None
            # attempt to
            try:
                # cast it into a date
                date = datetime.datetime.strptime(value, self.format).date()
            # if the parser refuses
            except (TypeError, ValueError) as error:
                # complain, passing along the parser's reason
                raise self.CastingError(value=value, description=self.complaint, error=error)
            # if all goes well, return the {date}
            return date
        # all other types are incompatible, for now
        raise self.CastingError(value=value, description=self.complaint)

    def string(self, value):
        """
        Render value as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # my value knows
        return value.strftime(self.format)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a date
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDate
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=datetime.date.today(), format=format, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file
