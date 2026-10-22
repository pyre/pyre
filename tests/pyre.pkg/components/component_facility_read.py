#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Reading a facility builds its component without changing the rank or the provenance of the
setting that decided it, so later settings compete with that setting as they would have before
the read
"""


def test() -> None:
    """
    Read a facility set on the command line and one left at its default, and check what the store
    says about each before and after the read, and how later settings fare
    """
    # support
    import pyre

    # get the executive
    executive = pyre.executive
    # and its store
    nameserver = executive.nameserver
    # the family of the components
    family = "pyre.tests.components.facility.read"

    # a command line that sets one of the facilities
    events = pyre.config.newCommandLineParser().parse([f"--c.t={family}.tools.saw"])
    # process it, at the rank of the command line
    executive.configurator.processEvents(events=events, priority=executive.priority.command)

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

    # another one
    class Saw(pyre.component, family=f"{family}.tools.saw", implements=Tool):
        """
        The tool the command line asks for
        """

    # a component with two facilities
    class Bench(pyre.component, family=f"{family}.bench"):
        """
        A component with a facility set on the command line, and one left at its default
        """

        # the facility the command line sets
        t = Tool()
        t.default = Hammer
        t.doc = "a facility set on the command line"

        # the facility left at its default
        u = Tool()
        u.default = Hammer
        u.doc = "a facility left at its default"

    # build the instance
    c = Bench(name="c")

    # go through the two facilities, with the rank each one starts with
    for name, rank in (("t", executive.priority.command), ("u", executive.priority.defaults)):
        # what the store says before the read
        how = c.pyre_how(attribute=name)
        where = str(c.pyre_where(attribute=name))
        # the rank is that of the setting that decided the facility
        assert how.category == rank.category, (name, how)
        # read the facility, which builds its component
        built = getattr(c, name)
        # the component is named after the facility
        assert built.pyre_name == f"c.{name}", (name, built.pyre_name)
        # and the store holds it under that name
        assert nameserver[f"c.{name}"] is built, name
        # the read changed neither the rank
        assert c.pyre_how(attribute=name) == how, (name, how, c.pyre_how(attribute=name))
        # nor the provenance of the setting
        assert str(c.pyre_where(attribute=name)) == where, (name, where)

    # the facility set on the command line holds a saw
    assert isinstance(c.t, Saw)
    # and the one left at its default, a hammer
    assert isinstance(c.u, Hammer)

    # a later setting ranked below the command line
    nameserver.insert(
        name="c.t",
        value=f"{family}.tools.hammer",
        priority=executive.priority.user(),
        locator=pyre.tracking.here(),
    )
    # loses to it, as it would have before the read
    assert isinstance(c.t, Saw)
    # while a later setting ranked above the default
    nameserver.insert(
        name="c.u",
        value=f"{family}.tools.saw",
        priority=executive.priority.user(),
        locator=pyre.tracking.here(),
    )
    # wins over it, as it would have before the read
    assert isinstance(c.u, Saw)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
