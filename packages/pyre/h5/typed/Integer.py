# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the {int} mixin
class Integer:
    """
    Implementation details of the {int} dataset mixin
    """

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # read the value
        value = self.pyre_id.int()
        # store it
        self.value = value
        # and return the raw contents
        return value


# end of file
