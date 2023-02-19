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
    def _pyre_pull(self, dataset):
        """
        Read my value from disk and update my cache
        """
        # read the value
        value = dataset._pyre_id.double()
        # and return the raw contents
        return value


# end of file
