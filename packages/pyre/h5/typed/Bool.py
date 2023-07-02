# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# types
from .. import libh5
from .. import disktypes
from .. import memtypes


# the {bool} mixin
class Bool:
    """
    Implementation details of the {bool} dataset mixin
    """

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(disktype=disktypes.c_s1, memtype=memtypes.int8, **kwds)
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value; values are stored as strings, for now
        value = dataset._pyre_id.str()
        # process it and return it
        return self.process(value)

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """
        # grab the value and convert to a string
        value = str(src.value)
        # and write it out
        dst.str(value)
        # all done
        return


# end of file
