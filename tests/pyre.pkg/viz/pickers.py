#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A picker reads the contents of a file and writes the dataset whose value along every axis is the
one in its selection; it suggests one selection per dataset, and refuses, naming the reason, a
selection that leaves an axis out or that no dataset matches; the contents and the dataset
describe what they hold to whoever inspects them
"""


def test() -> None:
    """
    Pick datasets out of contents with two axes, one of which has a value no dataset holds
    """
    # support
    import pyre

    # the contents of a file with two frequencies and two polarizations, but no B/VV
    contents = pyre.viz.contents.memory()(name="tests.pyre.viz.pickers.contents")
    contents.fill(
        axes={"frequency": ("A", "B"), "polarization": ("HH", "VV")},
        entries=[
            {"selector": {"frequency": "A", "polarization": "HH"}, "source": "A/HH"},
            {"selector": {"frequency": "A", "polarization": "VV"}, "source": "A/VV"},
            {"selector": {"frequency": "B", "polarization": "HH"}, "source": "B/HH"},
        ],
    )
    # the values present are the ones the datasets hold
    assert contents.present() == {"frequency": {"A", "B"}, "polarization": {"HH", "VV"}}
    # and they describe their axes, then their datasets
    assert list(contents.pyre_describe()) == [
        ("frequency", "A, B"),
        ("polarization", "HH, VV"),
        ("dataset", "frequency=A, polarization=HH"),
        ("dataset", "frequency=A, polarization=VV"),
        ("dataset", "frequency=B, polarization=HH"),
    ], list(contents.pyre_describe())

    # a picker, bound to them
    picker = pyre.viz.pickers.match()(name="tests.pyre.viz.pickers.match")
    picker.contents = contents
    # suggests one selection per dataset
    suggestions = list(picker.pyre_suggest(trait=picker.pyre_trait(alias="selection")))
    assert suggestions == [entry["selector"] for entry in contents.entries], suggestions
    # and nothing for its other traits
    assert not list(picker.pyre_suggest(trait=picker.pyre_trait(alias="contents")))

    # a selection that names every axis
    picker.selection = {"frequency": "B", "polarization": "HH"}
    # picks the dataset that matches it
    picker.pyre_run()
    assert picker.dataset.selector == {"frequency": "B", "polarization": "HH"}
    assert picker.dataset.source == "B/HH", picker.dataset.source
    # which describes itself by its value along every axis, and its source
    assert list(picker.dataset.pyre_describe()) == [
        ("frequency", "B"),
        ("polarization", "HH"),
        ("source", "B/HH"),
    ], list(picker.dataset.pyre_describe())

    # a selection that leaves an axis out
    picker.selection = {"frequency": "A"}
    # is refused, naming the axis
    try:
        picker.pyre_run()
        assert False, "a selection that leaves an axis out was accepted"
    except pyre.flow.exceptions.ProductionError as error:
        assert error.product == "dataset" and "polarization" in error.reason, error.reason
    # and leaves the dataset as it was
    assert picker.dataset.source == "B/HH", picker.dataset.source

    # a selection no dataset matches
    picker.selection = {"frequency": "B", "polarization": "VV"}
    # is refused too
    try:
        picker.pyre_run()
        assert False, "a selection no dataset matches was accepted"
    except pyre.flow.exceptions.ProductionError as error:
        assert error.product == "dataset" and "no dataset matches" in error.reason, error.reason

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
