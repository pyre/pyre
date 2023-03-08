# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import pyre

# types
from .. import disktypes


# the {bool} mixin
class Bool:
    """
    Implementation details of the {bool} dataset mixin
    """

    # type info
    disktype = disktypes.strType
    memtype = None

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value; values are stored as strings, for now
        value = dataset._pyre_id.str()
        # process it and return it
        return self.process(value)

    def _pyre_push(self, src, dest):
        """
        Push my cache value to disk
        """
        # grab the value and convert to a string
        value = str(src.value)
        # and write it out
        dest._pyre_id.str(value)
        # all done
        return


# end of file
