#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The contents of a file hand out a selector that solves selections over their axes: for a partial
selection it says which values of each axis are chosen, which can still be reached given the
values chosen for the other axes, and which are ruled out; it picks the dataset a complete
selection names, and says why a selection picks none
"""


def test() -> None:
    """
    Solve selections over contents with two axes, one of which has a value no dataset holds
    """
    # support
    import pyre

    # the contents of a file with two frequencies and two polarizations, but no B/VV
    contents = pyre.viz.contents.memory()(name="tests.pyre.viz.selector.contents")
    # filled with the axes and the datasets of such a file
    contents.fill(
        axes={"frequency": ("A", "B"), "polarization": ("HH", "VV")},
        entries=[
            {"selector": {"frequency": "A", "polarization": "HH"}, "source": "A/HH"},
            {"selector": {"frequency": "A", "polarization": "VV"}, "source": "A/VV"},
            {"selector": {"frequency": "B", "polarization": "HH"}, "source": "B/HH"},
        ],
    )
    # get a selector
    selector = contents.selector()
    # and the names of the states
    chosen, reachable, excluded = selector.chosen, selector.reachable, selector.excluded

    # with nothing chosen, every value some dataset holds can be reached
    assert selector.states(selection={}) == {
        "frequency": {"A": reachable, "B": reachable},
        "polarization": {"HH": reachable, "VV": reachable},
    }, selector.states(selection={})
    # and the selection is refused, naming both axes
    assert selector.refusal(selection={}) == "the selection names no frequency or polarization"

    # choosing B rules out VV, which no B dataset holds, but leaves A within reach
    assert selector.states(selection={"frequency": "B"}) == {
        "frequency": {"A": reachable, "B": chosen},
        "polarization": {"HH": reachable, "VV": excluded},
    }, selector.states(selection={"frequency": "B"})
    # and the selection is refused, naming the axis left out
    assert selector.refusal(selection={"frequency": "B"}) == "the selection names no polarization"
    # and picks nothing
    assert selector.pick(selection={"frequency": "B"}) is None

    # a complete selection
    selection = {"frequency": "B", "polarization": "HH"}
    # keeps the other frequency within reach, since A/HH exists
    assert selector.states(selection=selection) == {
        "frequency": {"A": reachable, "B": chosen},
        "polarization": {"HH": chosen, "VV": excluded},
    }, selector.states(selection=selection)
    # is not refused
    assert selector.refusal(selection=selection) is None
    # and picks its dataset
    assert selector.pick(selection=selection)["source"] == "B/HH"

    # a complete selection no dataset holds
    selection = {"frequency": "B", "polarization": "VV"}
    # shows each axis the way out: the values that agree with the choice on the other axis
    assert selector.states(selection=selection) == {
        "frequency": {"A": reachable, "B": chosen},
        "polarization": {"HH": reachable, "VV": chosen},
    }, selector.states(selection=selection)
    # is refused, saying nothing matches
    assert (
        selector.refusal(selection=selection)
        == "no dataset matches the selection frequency=B, polarization=VV"
    ), selector.refusal(selection=selection)
    # and picks nothing
    assert selector.pick(selection=selection) is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
