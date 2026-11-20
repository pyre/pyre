#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check how the pfg mill renders containers: a list puts its items on lines of their own, a list
nested in a list fits on the line of its item, and a mapping fits on one line, with its values
"""


def test() -> None:
    """
    Render a list, a list of lists, and a mapping
    """
    # support
    import pyre

    # make a mill
    mill = pyre.weaver.pfg()(name="mill")

    # a list of strings
    strings = pyre.schemata.list(schema=pyre.schemata.str())
    # named the way a trait would be
    strings.name = "strings"
    # render it
    rendered = list(strings._pyre_identify(authority=mill, value=["a", "b"], workload=[]))
    # it puts its name on a line, and each of its items on a line of its own
    assert rendered == ["strings = ", "a,", "b,"], rendered

    # a list of lists of strings
    nested = pyre.schemata.list(schema=pyre.schemata.list(schema=pyre.schemata.str()))
    # named the way a trait would be
    nested.name = "nested"
    # render it
    rendered = list(nested._pyre_identify(authority=mill, value=[["a", "b"]], workload=[]))
    # each inner list fits on the line of its item
    assert rendered == ["nested = ", "a, b,"], rendered

    # a mapping of strings
    mapping = pyre.schemata.mapping(schema=pyre.schemata.str())
    # named the way a trait would be
    mapping.name = "selection"
    # a selection
    value = {"band": "L", "frequency": "A"}
    # render it
    rendered = list(mapping._pyre_identify(authority=mill, value=value, workload=[]))
    # it fits on one line, in its text form
    assert rendered == ["selection = band:L, frequency:A"], rendered

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
