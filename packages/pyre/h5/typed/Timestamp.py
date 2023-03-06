# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre


# the {timestamp} mixin
class Timestamp:
    """
    Implementation details of the {timestamp} dataset mixin
    """

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value; timestamps are stored as strings
        value = dataset._pyre_id.str()
        # process it and return it
        return self.process(value[:26])

    def _pyre_push(self, src, dest):
        """
        Push my cache value to disk
        """
        # grab the value
        value = src.value
        # and write it out
        dest._pyre_id.str(value)
        # all done
        return


# end of file
