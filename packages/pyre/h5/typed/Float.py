# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the {float} mixin
class Float:
    """
    Implementation details of the {float} dataset mixin
    """

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # read the value
        value = self.pyre_id.double()
        # store it
        self.value = value
        # and return the raw contents
        return value


# end of file
