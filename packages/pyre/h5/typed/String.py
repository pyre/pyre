# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# types
from .. import disktypes
from .. import memtypes


# the {str} mixin
class String:
    """
    Implementation details of the {str} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=memtypes.char, disktype=disktypes.char, **kwds):
        # chain up
        super().__init__(memtype=memtype, disktype=disktype, **kwds)
        # all done
        return

    # representations
    def string(self, value):
        """
        Quote my value
        """
        return f"'{value}'"

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value
        value = dataset._pyre_id.str()
        # and return the raw contents
        return value

    def _pyre_push(self, src, dest):
        """
        Push my cache value to disk
        """
        # grab the value
        value = src.value
        # and write it out
        dest._pyre_id.str(value)
        # all done
        return


# end of file
