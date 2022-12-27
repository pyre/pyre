# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the {timestamp} mixin
class Timestamp:
    """
    Implementation details of the {timestamp} dataset mixin
    """

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # read the value; timestamps are stored as strings
        value = self.pyre_id.str()
        # store it; drop nanosecond precision since {strptime} can't handle it
        self.value = value[:26]
        # and return the raw contents
        return value

    # framework hooks
    def pyre_clone(self, format=None, **kwds):
        """
        Make a copy of my
        """
        # chain up
        return super().pyre_clone(format=self.format, **kwds)


# end of file
