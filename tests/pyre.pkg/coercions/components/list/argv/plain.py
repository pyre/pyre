#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that setting a list of components to 'pyre.tests.none.widgets.gadget,
pyre.tests.none.widgets.gadget' on the command line: every element is an instance of the named
component, as a facility would hold
"""


def test() -> None:
    """
    Parse a command line that sets the trait to 'pyre.tests.none.widgets.gadget,
    pyre.tests.none.widgets.gadget', make the instance, and read it
    """
    # access the framework
    import pyre

    # access the executive
    executive = pyre.executive
    # the command line
    commandline = ["--c.t=pyre.tests.none.widgets.gadget, pyre.tests.none.widgets.gadget"]
    # parse it
    events = pyre.config.newCommandLineParser().parse(commandline)
    # process the assignments it holds, which must go through without complaint
    assert not executive.configurator.processEvents(
        events=events, priority=executive.priority.command
    )

    # a protocol
    class widget(pyre.protocol, family="pyre.tests.none.widgets"):
        """a protocol for the components the trait holds"""

    # a component that implements it, which the command line names by its family
    class gadget(pyre.component, family="pyre.tests.none.widgets.gadget", implements=widget):
        """a component the trait can hold"""

    # a component with a list of components
    class component(pyre.component):
        """a component with a list of components"""

        # the trait
        t = pyre.properties.list(schema=widget())

    # make the instance the command line configures
    c = component(name="c")
    # every element is an instance of the named component, as a facility would hold
    assert len(c.t) == 2 and all(isinstance(e, gadget) for e in c.t)
    # the setting took effect, at the rank of its source
    assert c.pyre_how(attribute="t").category == pyre.executive.priority.command.category

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
