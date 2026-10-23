#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that setting a str trait to 'nOnE' on the command line leaves it unset
"""


def test() -> None:
    """
    Parse a command line that sets the trait to 'nOnE', make the instance, and read it
    """
    # access the framework
    import pyre

    # access the executive
    executive = pyre.executive
    # the command line
    commandline = ["--c.t=nOnE"]
    # parse it
    events = pyre.config.newCommandLineParser().parse(commandline)
    # process the assignments it holds, which must go through without complaint
    assert not executive.configurator.processEvents(
        events=events, priority=executive.priority.command
    )

    # a component with a str trait
    class component(pyre.component):
        """a component with a str trait"""

        # the trait
        t = pyre.properties.str()

    # make the instance the command line configures
    c = component(name="c")
    # the setting took effect, at the rank of its source
    assert c.pyre_how(attribute="t").category == pyre.executive.priority.command.category
    # the trait is unset
    assert c.t is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
