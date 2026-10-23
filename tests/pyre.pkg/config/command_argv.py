#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the pyre executive can communicate with external command line parsers
"""


def test():
    # get the package
    import pyre

    # access the executive instance
    executive = pyre.executive
    # pull the configurator
    configurator = executive.configurator
    # the nameserver
    nameserver = executive.nameserver
    # and a command line parser
    parser = pyre.config.newCommandLineParser()

    # build an argument list
    commandline = [
        "--help",
        "--vtf.nodes=1024",
        "--vtf.(solid,fluid)=solvers",
        "--vtf.(solid,fluid,other).nodes={vtf.nodes}",
        "--journal.debug.main=on",
        "--",
        "--funky-filename",
        "and-a-normal-one",
    ]

    # get the parser to populate the configurator
    events = parser.parse(commandline)
    # and transfer the events to the configurator
    configurator.processEvents(events=events, priority=executive.priority.user)

    # check that the assignments took place, starting with the bare flag
    assert nameserver["help"] == ""
    # the plain assignment
    assert nameserver["vtf.nodes"] == "1024"
    # the assignment to a group of keys reached both of them
    assert nameserver["vtf.solid"] == "solvers"
    # including the second one
    assert nameserver["vtf.fluid"] == "solvers"
    # the reference to another key was resolved
    assert nameserver["vtf.solid.nodes"] == "1024"
    # for every member of the group
    assert nameserver["vtf.fluid.nodes"] == "1024"
    # including the last one
    assert nameserver["vtf.other.nodes"] == "1024"
    # the journal setting
    assert nameserver["journal.debug.main"] == "on"
    # and the arguments after the end of the options are left for the application
    assert [event.command for event in configurator.consumeCommands()] == [
        "--funky-filename",
        "and-a-normal-one",
    ]

    # and return the managers
    return executive, parser


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
