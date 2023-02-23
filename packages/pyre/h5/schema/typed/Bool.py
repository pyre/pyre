# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import pyre


# the {bool} mixin
class Bool:
    """
    Implementation details of the {bool} dataset mixin
    """

    # type info
    disktype = pyre.libh5.datatypes.StrType
    memtype = None

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value; values are stored as strings, for now
        value = dataset._pyre_id.str()
        # and return the raw contents
        return value


# end of file
