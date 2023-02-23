# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# parts
from .Raster import Raster


# the {array} mixin
class Array:
    """
    Implementation details of the {array} dataset mixin
    """

    # type info
    @property
    def disktype(self):
        """
        Extract the on-disk type of my schema
        """
        # easy enough
        return self.schema.disktype

    @property
    def memtype(self):
        """
        Extract the in-memory type of my schema
        """
        # easy enough
        return self.schema.memtype

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into an array

        This is sufficiently high up in the conversion process to suffice; the only thing higher
        is {process}, and its implementation in {schema} just delegates to {coerce} immediately
        """
        # leave alone, for now
        return value

    # framework hooks value synchronization
    def _pyre_pull(self, dataset):
        """
        Build a proxy to help with the file interactions
        """
        # build my value
        value = Raster(dataset=dataset, schema=self.schema)
        # and return it
        return value


# end of file
