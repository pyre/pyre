# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Contents import Contents


# the contents of a file, held in memory
class Memory(pyre.flow.product, family="pyre.viz.contents.memory", implements=Contents):
    """
    The contents of a file, held in memory: the axes that tell its datasets apart, with the
    values each one may take, and the datasets, each known by its value along every axis
    """

    # interface
    def fill(self, axes: dict, entries: list) -> "Memory":
        """
        Record the {axes} of a file, a map from the name of each axis to the values it may take,
        in order, and its {entries}, a list of the datasets it holds, each one a map with its
        value along every axis under {selector}, and whatever its reader knows about it
        """
        # record the axes, in their order
        self.axes = {axis: tuple(values) for axis, values in axes.items()}
        # and the entries
        self.entries = list(entries)
        # all done
        return self

    def present(self) -> dict:
        """
        The values of every axis that some dataset actually has, which may be fewer than the
        ones the axis may take
        """
        # collect them from the entries, so they can never disagree with them
        return {
            axis: {entry["selector"][axis] for entry in self.entries if axis in entry["selector"]}
            for axis in self.axes
        }

    def match(self, selection: dict) -> dict | None:
        """
        The entry whose value along every axis is the one in {selection}, if there is one
        """
        # look for it
        return next((entry for entry in self.entries if entry["selector"] == selection), None)

    # introspection
    def pyre_describe(self):
        """
        Describe my axes, each with the values it may take, and my datasets, each by its value
        along every axis
        """
        # go through the axes
        for axis, values in self.axes.items():
            # and list the values each may take
            yield axis, ", ".join(str(value) for value in values)
        # go through the datasets
        for entry in self.entries:
            # and describe each one by its value along every axis
            yield "dataset", ", ".join(
                f"{axis}={value}" for axis, value in entry["selector"].items()
            )
        # all done
        return

    # metamethods
    def __init__(self, **kwds) -> None:
        # chain up
        super().__init__(**kwds)
        # the axes, by name, with the values each may take
        self.axes = {}
        # and the datasets
        self.entries = []
        # all done
        return


# end of file
