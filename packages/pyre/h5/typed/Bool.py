# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the {bool} mixin
class Bool:
    """
    Implementation details of the {bool} dataset mixin
    """

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # read the value; values are stored as strings, for now
        value = self.pyre_id.str()
        # store it
        self.value = value
        # and return the raw contents
        return value


# end of file
