# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre


# the {complex} mixin
class Complex:
    """
    Implementation details of the {complex} dataset mixin
    """

    # metamethods
    def __init__(self, memtype=None, disktype=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # if the caller didn't specify a memtype
        if memtype is None:
            # set it to {std::complex<double>}
            memtype = pyre.h5.memtypes.complex128()
        # save my in-memory type
        self.memtype = memtype
        # similarly, if there is no disktype specification
        if disktype is None:
            # use a double as the basis
            double = pyre.h5.disktypes.float(pyre.libh5.datatypes.native.double)
            # to build a compound type
            disktype = pyre.h5.disktypes.compound(2 * double.bytes)
            # with a real part
            disktype.insert(name="r", offset=0, type=double)
            # and an imaginary part
            disktype.insert(name="i", offset=double.bytes, type=double)
        # save my on-disk type
        self.disktype = disktype
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value
        value = dataset._pyre_id.complex()
        # and return the raw contents
        return value


# end of file
