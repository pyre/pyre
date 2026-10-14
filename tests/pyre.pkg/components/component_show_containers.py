#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the display of a configuration goes into the components held by lists, tuples and
dicts, the way it goes into the component bound to a facility, and refers to a component met
again by name
"""


def test() -> None:
    """
    Display the configuration of a component whose containers hold components
    """
    # support
    import pyre

    # a protocol for the parts
    class part(pyre.protocol, family="pyre.tests.show.parts"):
        """
        What the parts implement
        """

    # a part
    class gear(pyre.component, family="pyre.tests.show.parts.gear", implements=part):
        """
        A part with a setting, and parts of its own
        """

        # a setting
        teeth = pyre.properties.int(default=12)
        # and more parts
        meshes = pyre.properties.list(schema=part())

    # a component with containers of parts
    class machine(pyre.component, family="pyre.tests.show.machine"):
        """
        A component with a list, a tuple and a dict of parts
        """

        # the containers
        train = pyre.properties.list(schema=part())
        pair = pyre.properties.tuple(schema=part())
        spares = pyre.properties.dict(schema=part())

    # make the parts
    first = gear(name="first")
    second = gear(name="second")
    third = gear(name="third")
    # the first two mesh with each other, which makes a cycle
    first.meshes = [second]
    second.meshes = [first]
    # make the machine
    engine = machine(name="engine")
    # and fill its containers
    engine.train = [first, second]
    engine.pair = (third,)
    engine.spares["spare"] = gear(name="spare")

    # display the configuration
    display = list(engine.pyre_showConfiguration(deep=True))
    # the names on their own lines, which is how the display introduces a component
    names = [line.strip() for line in display if line.strip().endswith(":")]
    # every part held by a container is described
    for name in ("first", "second", "third", "spare"):
        # once
        assert names.count(f"{name}:") == 1, (name, display)
    # with its settings
    assert sum("value: 12" in line for line in display) == 4, display
    # and the part met again through the cycle is referred to by name
    assert any(line.strip() == "see first" for line in display), display

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
