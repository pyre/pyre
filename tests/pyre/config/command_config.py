#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that additional configuration files can be specified on the command line
"""


def test():
    import pyre
    # get the executive instance
    executive = pyre.executive
    # pull the configutor
    configurator = executive.configurator
    # and build a command line parser
    parser = executive.newCommandLineParser()
    # build an argument list
    commandline = [
        '--config=sample.pml',
        ]
    # get the parser to populate the configurator
    configuration = parser.decode(commandline)
    # and transfer the events to the configurator
    configurator.configure(configuration=configuration, priority=executive.USER_CONFIGURATION)
    # now, check that the assignments took place
    assert configurator["sample.user.name"] == "michael a.g. aïvázis"
    assert configurator["sample.user.email"] == "aivazis@caltech.edu"
    # and return the managers
    return parser


# main
if __name__ == "__main__":
    test()


# end of file 
