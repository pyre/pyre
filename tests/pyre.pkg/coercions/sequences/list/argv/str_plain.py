#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that setting a list trait whose elements are declared with a property to 'p, q' on the command
line gives the list, as a control for the element form
"""


def test() -> None:
    """
    Parse a command line that sets the trait to 'p, q', make the instance, and read it
    """
    # access the framework
    import pyre

    # access the executive
    executive = pyre.executive
    # the command line
    commandline = ["--c.t=p, q"]
    # parse it
    events = pyre.config.newCommandLineParser().parse(commandline)
    # process the assignments it holds, which must go through without complaint
    assert not executive.configurator.processEvents(
        events=events, priority=executive.priority.command
    )

    # a component with a list trait whose elements are declared with a property
    class component(pyre.component):
        """a component with a list trait whose elements are declared with a property"""

        # the trait
        t = pyre.properties.list(schema=pyre.properties.str())

    # make the instance the command line configures
    c = component(name="c")
    # the setting took effect, at the rank of its source
    assert c.pyre_how(attribute="t").category == pyre.executive.priority.command.category
    # the list is what the command line says
    assert c.t == ["p", "q"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
