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
    A type declarator for times of day

    My {timezone} says whether my values carry the offset of their time zone: {True} insists that
    they do, {False} that they do not, and {None} accepts either. Without a {format}, my text is
    the ISO 8601 form, which keeps the fraction of the second and the offset
    """

    # constants
    format = None  # the format of my text; {None} for the ISO 8601 form
    typename = "time"  # the name of my type
    complaint = "could not coerce {0.value!r} into a time"  # what i say when i refuse a value
    zoned = "could not coerce {0.value!r} into a time with a time zone"  # one without a zone
    naive = "could not coerce {0.value!r} into a time without a time zone"  # one with a zone

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a time of day
        """
        # perhaps {value} is already a {time} instance
        if isinstance(value, datetime.time):
            # in which case make sure it agrees with me about its zone
            return self._zone(value=value)
        # or a moment, whose time of day i keep, along with its zone
        if isinstance(value, datetime.datetime):
            # extract it and check it
            return self._zone(value=value.timetz())
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
                time = self._parse(text=value)
            # if the parser refuses
            except (TypeError, ValueError) as error:
                # complain, passing along the parser's reason
                raise self.CastingError(value=value, description=self.complaint, error=error)
            # if all goes well, make sure it agrees with me about its zone
            return self._zone(value=time)
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
        # without a format of my own
        if self.format is None:
            # write the ISO 8601 form
            return value.isoformat()
        # otherwise, my format knows
        return value.strftime(self.format)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # implementation details
    def _parse(self, text):
        """
        Read a time of day out of {text}
        """
        # without a format of my own
        if self.format is None:
            # read the ISO 8601 form
            return datetime.time.fromisoformat(text)
        # otherwise, my format knows
        return datetime.datetime.strptime(text, self.format).timetz()

    def _zone(self, value):
        """
        Make sure that {value} carries the offset of its time zone exactly when i say it must
        """
        # if i accept either kind
        if self.timezone is None:
            # there is nothing to check
            return value
        # whether {value} knows its offset
        aware = value.utcoffset() is not None
        # if it agrees with me
        if aware == self.timezone:
            # it is good
            return value
        # otherwise, complain about the kind it should have been
        raise self.CastingError(
            value=value, description=self.zoned if self.timezone else self.naive
        )

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a time of day
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
    def __init__(self, default=datetime.datetime.today(), format=format, timezone=None, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # store the format
        self.format = format
        # and what i say about time zones
        self.timezone = timezone
        # all done
        return


# end of file
