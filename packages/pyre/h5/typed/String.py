# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import pyre


# the {str} mixin
class String:
    """
    Implementation details of the {str} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=None, disktype=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my in-memory type
        self.memtype = memtype if memtype is not None else pyre.h5.memtypes.char()
        # save my on-disk type
        self.disktype = disktype if disktype is not None else pyre.h5.disktypes.str()
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value
        value = dataset._pyre_id.str()
        # and return the raw contents
        return value

    # representations
    def string(self, value):
        """
        Quote my value
        """
        return f"'{value}'"


# end of file
