# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# types
from .. import libh5
from .. import disktypes
from .. import memtypes


# the {enum} mixin
class Enum:
    """
    Implementation details of the {enum} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=memtypes.int32, disktype=disktypes.enumType, **kwds):
        # chain up
        super().__init__(memtype=memtype, disktype=disktype, **kwds)
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """


# end of file
