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

    # get a raw executive instance
    from pyre.framework.Executive import Executive
    executive = Executive()
    # pul the configutor and calculator
    calculator = executive.calculator
    configurator = executive.configurator
    # and a command line parser
    parser = pyre.config.newCommandLineParser()

    # build an argument list
    commandline = [
        '--config=sample.pml',
        ]

    # get the parser to populate the configurator
    parser.decode(configurator, commandline)
    # and transfer the events to the calculator
    configurator.configure(executive)
    # now, check that the assignments took place
    assert calculator["sample.user.name"] == "michael a.g. aïvázis"
    assert calculator["sample.user.email"] == "aivazis@caltech.edu"
    # and return the managers
    return executive, parser

# main
if __name__ == "__main__":
    test()


# end of file 
