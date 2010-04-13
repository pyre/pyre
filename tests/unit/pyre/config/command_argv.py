#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the command line parser can be instantiated
"""


def test():
    import pyre.config

    # build a new configurator
    configurator = pyre.config.newConfigurator()
    # a new calculator
    calculator = pyre.config.newCalculator()
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
    parser.decode(configurator, commandline)
    # and transfer the events to the calculator
    configurator.populate(calculator)
    # now, check that the assignments took place
    assert calculator["help"] == None
    assert calculator["vtf.nodes"] == "1024"
    assert calculator["vtf.solid"] == "solvers"
    assert calculator["vtf.fluid"] == "solvers"
    assert calculator["vtf.solid.nodes"] == "1024"
    assert calculator["vtf.fluid.nodes"] == "1024"
    assert calculator["journal.device"] == "file"
    assert calculator["journal.debug.main"] == "on"

    # and return the managers
    return calculator, configurator, parser

# main
if __name__ == "__main__":
    test()


# end of file 
