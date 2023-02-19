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
    def _pyre_pull(self, dataset):
        """
        Read my value from disk and update my cache
        """
        # read the value; timestamps are stored as strings
        value = dataset._pyre_id.str()
        # and return the raw contents
        return value[:26]


# end of file
