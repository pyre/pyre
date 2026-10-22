#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A facility switched to another component gives the new component its own defaults, not the
defaults of the component it replaced; a setting someone made under the facility survives the
switch
"""


def test() -> None:
    """
    Read a facility, switch it to another component, and check the traits of the new one
    """
    # support
    import pyre

    # get the store
    nameserver = pyre.executive.nameserver
    # the family of the components
    family = "pyre.tests.components.facility.switch"

    # a protocol for the tools
    class Tool(pyre.protocol, family=f"{family}.tools"):
        """
        The protocol of the tools
        """

    # a tool
    class Hammer(pyre.component, family=f"{family}.tools.hammer", implements=Tool):
        """
        The tool of the class
        """

        # its weight
        weight = pyre.properties.int()
        weight.default = 1
        weight.doc = "the weight of a hammer"

        # its color
        color = pyre.properties.str()
        color.default = "black"
        color.doc = "the color of a hammer"

    # another tool, with traits of the same names and defaults of its own
    class Saw(pyre.component, family=f"{family}.tools.saw", implements=Tool):
        """
        The tool the facility switches to
        """

        # its weight
        weight = pyre.properties.int()
        weight.default = 2
        weight.doc = "the weight of a saw"

        # its color
        color = pyre.properties.str()
        color.default = "silver"
        color.doc = "the color of a saw"

    # a component with a facility
    class Bench(pyre.component, family=f"{family}.bench"):
        """
        A component with a facility
        """

        # the facility
        tool = Tool()
        tool.default = Hammer
        tool.doc = "the tool on the bench"

    # someone sets the color of whatever tool the bench holds
    nameserver["w.tool.color"] = "red"
    # build the bench
    w = Bench(name="w")
    # read its tool, a hammer with its own weight
    assert isinstance(w.tool, Hammer) and w.tool.weight == 1
    # and the color that was set
    assert w.tool.color == "red"

    # switch the tool
    w.tool = Saw
    # the new tool is a saw
    assert isinstance(w.tool, Saw)
    # with its own weight, not the hammer's
    assert w.tool.weight == 2, w.tool.weight
    # and the color that was set, which outranks both defaults
    assert w.tool.color == "red", w.tool.color

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
