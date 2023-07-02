# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# types
from .. import libh5
from .. import disktypes
from .. import memtypes


# the {str} mixin
class String:
    """
    Implementation details of the {str} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=memtypes.char, disktype=disktypes.strType, **kwds):
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
        value = dataset._pyre_id.str()
        # and return the raw contents
        return value

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """
        # grab the value
        value = self.string(src.value)
        # and write it out
        dst.str(value)
        # all done
        return

    # information about my on-disk layout
    def _pyre_describe(self, dataset):
        """
        Construct representations for my on-disk datatype and dataspace
        """
        # strings are scalars
        shape = libh5.DataSpace()
        # but the type knows the length of the value
        type = self.disktype(cells=max(1, len(self.string(dataset.value))))
        # hand off the pair
        return type, shape, None


# end of file
