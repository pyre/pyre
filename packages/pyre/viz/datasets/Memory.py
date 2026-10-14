# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Dataset import Dataset


# a dataset, held in memory
class Memory(pyre.flow.product, family="pyre.viz.datasets.memory", implements=Dataset):
    """
    One of the datasets of a file, held in memory: its value along every axis of the contents of
    the file, and whatever its reader knows about it
    """

    # interface
    def fill(self, selector: dict, source=None) -> "Memory":
        """
        Record the value of the dataset along every axis in {selector}, and its {source}, the
        object its reader keeps for it
        """
        # record the selector
        self.selector = dict(selector)
        # and the source
        self.source = source
        # all done
        return self

    # introspection
    def pyre_describe(self):
        """
        Describe my value along every axis, and the object my reader keeps for me
        """
        # go through my value along every axis
        for axis, value in self.selector.items():
            # and describe each one
            yield axis, str(value)
        # and the object my reader keeps for me, once there is one
        if self.source is not None:
            # describe it the way it prints
            yield "source", str(self.source)
        # all done
        return

    # metamethods
    def __init__(self, **kwds) -> None:
        # chain up
        super().__init__(**kwds)
        # the value of the dataset along every axis
        self.selector = {}
        # and the object its reader keeps for it, once there is one
        self.source = None
        # all done
        return


# end of file
