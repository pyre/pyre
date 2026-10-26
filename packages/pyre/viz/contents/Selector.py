# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# solve selections over the axes and the datasets of some contents
class Selector:
    """
    Solve selections over the axes of some contents and the datasets they hold: for a partial
    selection, say which values of each axis are chosen, which can still be reached and which
    are ruled out, and pick the dataset a complete selection names, or say why there is none
    """

    # the state of a value of an axis named by the selection
    chosen = "chosen"
    # of one some dataset holds along with the values chosen for the other axes
    reachable = "reachable"
    # and of one no such dataset holds
    excluded = "excluded"

    # interface
    def states(self, selection: dict) -> dict:
        """
        Classify the values of every axis under {selection}: the value it names for an axis is
        chosen; any other value is reachable when some dataset holds it along with the values
        {selection} names for the other axes, and excluded otherwise
        """
        # the table, one entry per axis, with the state of each of its values, in order
        table = {}
        # go through the axes
        for axis, values in self.axes.items():
            # the values chosen for the other axes constrain this one
            others = {name: value for name, value in selection.items() if name != axis}
            # the values of this axis held by the datasets that agree with them
            held = {
                entry["selector"].get(axis)
                for entry in self.entries
                if self._agrees(entry=entry, selection=others)
            }
            # classify each value of the axis
            table[axis] = {
                value: (
                    self.chosen
                    if selection.get(axis) == value
                    else self.reachable if value in held else self.excluded
                )
                for value in values
            }
        # hand the table off
        return table

    def pick(self, selection: dict) -> dict | None:
        """
        The dataset whose value along every axis is the one in {selection}, if there is one
        """
        # look for it
        return next((entry for entry in self.entries if entry["selector"] == selection), None)

    def refusal(self, selection: dict) -> str | None:
        """
        Why {selection} picks no dataset, the way a person would read it, or nothing when it
        picks one
        """
        # the axes it leaves out
        missing = [axis for axis in self.axes if axis not in selection]
        # if there are any
        if missing:
            # name them the way a person would list them
            axes = (
                ", ".join(missing[:-1]) + " or " + missing[-1] if len(missing) > 1 else missing[0]
            )
            # nothing can be picked, until the selection names a value for each of them
            return f"the selection names no {axes}"
        # if a dataset matches
        if self.pick(selection=selection) is not None:
            # there is nothing to explain
            return None
        # otherwise, the selection, the way it reads
        named = ", ".join(f"{axis}={value}" for axis, value in selection.items())
        # names a dataset that is not there
        return f"no dataset matches the selection {named}"

    # metamethods
    def __init__(self, axes: dict, entries: list, **kwds) -> None:
        # chain up
        super().__init__(**kwds)
        # the axes, by name, with the values each may take, in order
        self.axes = axes
        # and the datasets, each known by its value along every axis
        self.entries = entries
        # all done
        return

    # implementation details
    def _agrees(self, entry: dict, selection: dict) -> bool:
        """
        Check whether the dataset in {entry} holds every value in {selection}
        """
        # get its value along every axis
        selector = entry["selector"]
        # it agrees when it has the selected value along every selected axis
        return all(selector.get(axis) == value for axis, value in selection.items())


# end of file
