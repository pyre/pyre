# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .Descriptor import Descriptor


# the base class for all leaves
@pyre.schemata.typed
class Dataset(Descriptor):
    """
    The base class of all typed datasets
    """

    # metamethods
    def __init__(self, doc="", **kwds):
        # chain up
        super().__init__(**kwds)
        # record the documentation
        self.__doc__ = doc
        # all done
        return

    # representation
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"dataset '{self._pyre_name}' of type '{self.type}'"

    # framework hooks
    def _pyre_clone(self, default=object, **kwds):
        """
        Make a copy
        """
        # if i didn't get an explicit default value
        if default is object:
            # use mine
            default = self.default
        # add my state and chain up
        return super()._pyre_clone(default=default, doc=self.__doc__)

    # mixin for all sequences
    class containers:

        # hooks
        def _pyre_clone(self, **kwds):
            """
            Make a copy
            """
            # add my schema to the pile and chain up
            return super()._pyre_clone(
                schema=self.schema, default=self.container(self._default), **kwds
            )


# end of file
