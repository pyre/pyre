# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the {array} mixin
class Array:
    """
    Implementation details of the {array} dataset mixin
    """

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # get my id
        id = self.pyre_id
        # update my shape
        self.shape = id.shape
        # trivial, for now
        return self


# end of file
