#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that a sample configuration file can be ingested correctly
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()
    # verify the right parts were built
    assert executive.codex is not None
    assert executive.fileserver is not None
    assert executive.configurator is not None
    # load a configuration file
    executive.loadConfiguration(uri="sample.pml", priority=executive.USER_CONFIGURATION)
    # check that all is as expected
    assert executive.configurator["package.home"] == "home"
    assert executive.configurator["package.prefix"] == "prefix"
    assert executive.configurator["package.user.name"] == "michael a.g. aïvázis"
    assert executive.configurator["package.user.email"] == "aivazis@caltech.edu"
    assert executive.configurator["package.user.affiliation"] == "california institute of technology"

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
