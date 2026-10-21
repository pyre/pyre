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
class Time(Schema):
    """
    A type declarator for timestamps
    """

    # constants
    format = "%H:%M:%S"  # the default format
    typename = "time"  # the name of my type
    complaint = "could not coerce {0.value!r} into a time"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a timestamp
        """
        # perhaps {value} is already a {time} instance
        if isinstance(value, datetime.time):
            # in which case just return it
            return value
        # it might be a {datetime} instance
        if isinstance(value, datetime.datetime):
            # in which case extract a time object from it
            return value.timetz()
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
                # cast it into a time
                time = datetime.datetime.strptime(value, self.format).time()
            # if the parser refuses
            except (TypeError, ValueError) as error:
                # complain, passing along the parser's reason
                raise self.CastingError(value=value, description=self.complaint, error=error)
            # if all goes well, return the {time}
            return time
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
        Let {authority} know i am a time
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onTime
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=datetime.datetime.today(), format=format, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file
