#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check how the pfg mill renders a tree of components: each component gets a section, a facility
and the entries of a list of components are written as specifications, and every component they
refer to gets a section of its own after the one that refers to it
"""


def test() -> None:
    """
    Render a component with properties, a facility and a list of components
    """
    # support
    import pyre

    # a protocol for parts
    class Part(pyre.protocol, family="pyre.tests.weaver.pfg.parts"):
        """
        The obligations of parts
        """

        # the part to use when none is chosen
        @classmethod
        def pyre_default(cls, **kwds):
            """
            The default part
            """
            # is a gear
            return Gear

    # a part
    class Gear(pyre.component, family="pyre.tests.weaver.pfg.parts.gear", implements=Part):
        """
        A gear
        """

        # the number of teeth
        teeth = pyre.properties.int(default=12)

    # a machine made of parts
    class Machine(pyre.component, family="pyre.tests.weaver.pfg.machine"):
        """
        A machine
        """

        # a speed
        speed = pyre.properties.float(default=1.5)
        # a list of names
        names = pyre.properties.list(schema=pyre.properties.str(), default=["a", "b"])
        # a table
        table = pyre.properties.kv(default={"x": "1"})
        # the part it is built around
        gear = Part()
        # its spare parts
        spares = pyre.properties.list(schema=Part())

    # make a machine
    machine = Machine(name="machine")
    # with a spare part
    machine.spares = [Gear(name="spare")]
    # and a mill of configuration files
    mill = pyre.weaver.pfg()(name="mill")

    # render the machine
    rendered = list(machine.pyre_renderTraitValues(renderer=mill))
    # check the lines
    assert rendered == [
        # the section of the machine
        "pyre.tests.weaver.pfg.machine#machine:",
        "    speed = 1.5",
        "    names = ",
        "        a,",
        "        b,",
        "    table = x:1",
        "    gear = pyre.tests.weaver.pfg.parts.gear#machine.gear",
        "    spares = ",
        "        pyre.tests.weaver.pfg.parts.gear#spare,",
        "",
        # the section of the part it is built around
        "pyre.tests.weaver.pfg.parts.gear#machine.gear:",
        "    teeth = 12",
        "",
        # and the section of its spare part
        "pyre.tests.weaver.pfg.parts.gear#spare:",
        "    teeth = 12",
        "",
    ], rendered

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
