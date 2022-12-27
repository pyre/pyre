# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the {str} mixin
class String:
    """
    Implementation details of the {str} dataset mixin
    """

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # read the value
        value = self.pyre_id.str()
        # store it
        self.value = value
        # and return the raw contents
        return value

    # representations
    def string(self, value):
        """
        Quote my value
        """
        return f"'{value}'"


# end of file
