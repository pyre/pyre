# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# types
from .. import libh5
from .. import disktypes
from .. import memtypes


# the {int} mixin
class Integer:
    """
    Implementation details of the {int} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=memtypes.int64, disktype=disktypes.int64, **kwds):
        # chain up
        super().__init__(memtype=memtype, disktype=disktype, **kwds)
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

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """
        # grab the value
        value = src.value
        # and write it out
        dst.int(value)
        # all done
        return


# end of file
