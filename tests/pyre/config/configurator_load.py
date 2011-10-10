#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise loading settings from configuration files
"""


def test():
    import pyre
    
    # gain access to the configurator
    c = pyre.executive.configurator

    # attempt to request a node that doesn't exist yet
    try:
        c["sample.user.name"]
        assert False
    except c.UnresolvedNodeError:
        pass

    # this is the node that we build out of the configuration
    try:
        c["sample.user.byline"]
        assert False
    except c.UnresolvedNodeError:
        pass
    # so define it
    c["sample.user.byline"] = "{sample.user.name}+' -- '+{sample.user.email}"
    
    # load a configuration file
    pyre.loadConfiguration("sample.pml")
    # c.dump()

    # try again
    assert c["sample.user.name"] == "michael a.g. aïvázis"
    assert c["sample.user.email"] == "aivazis@caltech.edu"
    assert c["sample.user.affiliation"] == "california institute of technology"
    # and the local one
    assert c["sample.user.byline"] == "michael a.g. aïvázis -- aivazis@caltech.edu"

    return


# main
if __name__ == "__main__":
    test()


# end of file 
