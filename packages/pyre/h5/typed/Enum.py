# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# external
import enum
import journal

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
    def __init__(self, name, disktype, **kwds):
        # get the base type
        base = disktype.super
        # if it's not an integer type
        if not base.isA(libh5.DataSetType.int):
            # we have a problem
            channel = journal.firewall("pyre.h5.api.inspector")
            # complain
            channel.log(f"{name} is an enum based on a non-integral type")
            # and bail, in case firewalls aren't fatal
            return

        # cast to the actual int type
        base = disktypes.intType(base.hid)
        # deduce the correct in-memory representation
        sign = "u" if base.sign == libh5.Sign.unsigned else ""
        bits = base.precision
        # assemble the typename
        typename = f"{sign}int{bits}"
        # pull it
        memtype = getattr(memtypes, typename)

        # get the enum members
        members = sorted(disktype.map().items(), key=lambda item: item[1])
        # build the enumeration class
        cls = enum.Enum(
            name, names=[member[0] for member in members], start=members[0][1]
        )
        # chain up
        super().__init__(enum=cls, memtype=memtype, disktype=disktype, **kwds)

        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value
        value = dataset._pyre_id.enum()
        # and return it
        return self.enum(value)

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """
        # get my value
        value = src.value.value
        # and store it
        dst.pyre_id.enum(value)
        # all done
        return


# end of file
