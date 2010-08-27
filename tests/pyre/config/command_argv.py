#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the pyre executive can communicate with external command line parsers
"""


def test():
    import pyre.config

    # get the executive instance
    import pyre
    executive = pyre.executive
    # pull the configutor
    configurator = executive.configurator
    # and a command line parser
    parser = pyre.config.newCommandLineParser()

    # build an argument list
    commandline = [
        '--help',
        '--vtf.nodes=1024',
        '--vtf.(solid,fluid)=solvers',
        '--vtf.(solid,fluid,other).nodes={vtf.nodes}',
        '--journal.device=file',
        '--journal.debug.main=on',
        '--',
        '--funky-filename',
        'and-a-normal-one'
        ]

    # get the parser to populate the configurator
    configuration = parser.decode(commandline)
    # and transfer the events to the configurator
    configurator.configure(configuration=configuration, priority=executive.USER_CONFIGURATION)
    # dump the state
    # configurator._dump()
    # and check that the assignments took place
    assert configurator["help"] == None
    assert configurator["vtf.nodes"] == "1024"
    assert configurator["vtf.solid"] == "solvers"
    assert configurator["vtf.fluid"] == "solvers"
    assert configurator["vtf.solid.nodes"] == "1024"
    assert configurator["vtf.fluid.nodes"] == "1024"
    assert configurator["journal.device"] == "file"
    assert configurator["journal.debug.main"] == "on"

    # and return the managers
    return executive, parser

# main
if __name__ == "__main__":
    test()


# end of file 
