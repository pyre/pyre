# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import datetime
import math

# the bindings
from .. import libpyre


# the line of time, with the civil calendar
class Timeline:
    """
    The affine line of time, whose instants the civil calendar names; times without a time zone
    are read as UTC, and the times it hands out are in UTC
    """

    # the start of 1970, in UTC
    unix = datetime.datetime(1970, 1, 1, tzinfo=datetime.UTC)

    # interface
    def point(self, time: datetime.datetime):
        """
        The instant at {time}
        """
        # by its seconds past my epoch
        return self.line.point(coordinate=self.seconds(time=time))

    def time(self, point) -> datetime.datetime | None:
        """
        The time of the instant {point}, or nothing for the ends of the line, which are not on the
        calendar
        """
        # the seconds of the instant past my epoch
        coordinate = point.coordinate
        # the ends of the line
        if math.isinf(coordinate):
            # have no time
            return None
        # the others are my epoch moved by their seconds
        return self.epoch + datetime.timedelta(seconds=coordinate)

    def interval(
        self, begin: datetime.datetime | None = None, end: datetime.datetime | None = None
    ):
        """
        The instants from {begin} to {end}, both included; the interval is unbounded on the side
        whose time is missing
        """
        # the lower end, at the bottom of the line when there is no {begin}
        lower = -math.inf if begin is None else self.seconds(time=begin)
        # the upper end, at the top of the line when there is no {end}
        upper = math.inf if end is None else self.seconds(time=end)
        # the interval between them
        return self.line.interval(lower=lower, upper=upper)

    def seconds(self, time: datetime.datetime) -> float:
        """
        The seconds from my epoch to {time}
        """
        # measured in UTC
        return (self.utc(time=time) - self.epoch).total_seconds()

    @staticmethod
    def utc(time: datetime.datetime) -> datetime.datetime:
        """
        Express {time} in UTC; a time without a time zone already is
        """
        # a time without a time zone
        if time.tzinfo is None:
            # is in UTC
            return time.replace(tzinfo=datetime.UTC)
        # the others are converted
        return time.astimezone(datetime.UTC)

    # metamethods
    def __init__(self, epoch: datetime.datetime | None = None, **kwds):
        """
        Make a timeline with the given {epoch}, by default the start of 1970 in UTC
        """
        # chain up
        super().__init__(**kwds)
        # my epoch
        self.epoch = self.unix if epoch is None else self.utc(time=epoch)
        # and the line of the bindings, which knows its epoch by its seconds past the unix one
        self.line = libpyre.geometry.Timeline(epoch=(self.epoch - self.unix).total_seconds())
        # all done
        return


# end of file
