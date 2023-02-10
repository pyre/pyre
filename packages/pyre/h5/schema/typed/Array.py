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
    def _pyre_pull(self, dataset):
        """
        Read my value from disk and update my cache
        """
        # update my shape
        self.shape = dataset._pyre_id.shape
        # trivial, for now
        return self


# end of file
