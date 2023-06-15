# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import pyre

# types
from .. import libh5
from .. import disktypes
from .. import memtypes

# superclass
from .Descriptor import Descriptor


# the base class for all leaves
@pyre.schemata.typed
class Dataset(Descriptor):
    """
    The base class of all typed datasets
    """

    # my mixins
    from ..typed import array, bool, complex, float, int, str, timestamp, containers

    # metamethods
    # construction
    def __init__(self, memtype: memtypes.type, disktype: disktypes.type, **kwds):
        # chain up
        super().__init__(**kwds)
        # record my types
        self.memtype = memtype
        self.disktype = disktype
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
    # cloning
    # value syncing hooks by dataset subclasses
    def _pyre_pull(self, dataset):
        """
        Pull my on-disk value into my cache
        """
        # get my type
        cls = type(self)
        # my children must know how to do this
        raise NotImplementedError(
            f"class '{cls.__module__}.{cls.__name__}' must implement '_pyre_pull'"
        )

    def _pyre_push(self, src, dst):
        """
        Push my cache value to disk
        """
        # get my type
        cls = type(self)
        # my children must know how to do this
        raise NotImplementedError(
            f"class '{cls.__module__}.{cls.__name__}' must implement '_pyre_push'"
        )

    # a dataspace compatible with my type and my client's value
    def _pyre_describe(self, **kwds):
        """
        Construct representations for my on-disk datatype and dataspace
        """
        # all descriptors are assumed to be scalars, by default
        scalar = libh5.DataSpace()
        # as a result, their type does not depend on the value of the dataset
        type = self.disktype
        # hand off the pair
        return type, scalar, None

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDataset
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)

    # decoration
    def _pyre_marker(self):
        """
        Generate an identifying mark for structural renderings
        """
        # easy
        return self.type


# end of file
