# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the mixin for containers
class Container:
    """
    The base class for all container types
    """

    # framework hooks
    def _pyre_clone(self, **kwds):
        """
        Make a copy
        """
        # add my schema to the pile and chain up
        return super()._pyre_clone(
            schema=self.schema, default=self.container(self._default), **kwds
        )


# end of file
