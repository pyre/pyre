# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre


# the {int} mixin
class Integer:
    """
    Implementation details of the {int} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=None, disktype=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my in-memory type
        self.memtype = memtype if memtype is not None else pyre.h5.memtypes.int64()
        # save my on-disk type
        self.disktype = disktype if disktype is not None else pyre.h5.disktypes.int()
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value
        value = dataset._pyre_id.int()
        # and return the raw contents
        return value

    def _pyre_push(self, src, dest):
        """
        Push my cache value to disk
        """
        # grab the value
        value = src.value
        # and write it out
        dest._pyre_id.int(value)
        # all done
        return


# end of file
