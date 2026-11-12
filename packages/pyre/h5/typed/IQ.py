# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the hdf5 types
from .. import disktypes
from .. import memtypes


# a radar sample: a pair of integer counts
class IQ:
    """
    Implementation details of the {iq} dataset mixin, a radar sample made of its in-phase and
    quadrature counts
    """

    # metamethods
    def __init__(self, memtype=memtypes.iqInt64, disktype=disktypes.iqInt64, **kwds):
        # chain up; a value is converted the way a tuple of integers is
        super().__init__(memtype=memtype, disktype=disktype, schema=pyre.schemata.int(), **kwds)
        # all done
        return

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a sample, the pair of its counts
        """
        # convert it the way a tuple of integers is converted
        sample = super().coerce(value=value, **kwds)
        # a sample has exactly two counts
        if len(sample) != 2:
            # so anything else is not one
            raise self.CastingError(value=value, description="a sample has exactly two counts")
        # all done
        return sample

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value, as the pair of its counts
        value = dataset._pyre_id.iq()
        # and return it
        return value


# end of file
