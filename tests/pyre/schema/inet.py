#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise the internet address parser
"""


def test():
    # get the package parts
    from pyre.schema.INet import (
        IPv4 as ipv4,
        Unix as unix,
        Parser as parser)

    # positive tests
    # ip4 with full information
    address = parser.parse("ip4:pyre.caltech.edu:50000")
    assert address.family == ipv4.family
    assert address.host == "pyre.caltech.edu"
    assert address.port == 50000
    assert address.value == ("pyre.caltech.edu", 50000)

    # ip4 with no family
    address = parser.parse("ip4:pyre.caltech.edu:50000")
    assert address.family == ipv4.family
    assert address.host == "pyre.caltech.edu"
    assert address.port == 50000
    assert address.value == ("pyre.caltech.edu", 50000)

    # ip4 with no port
    address = parser.parse("ip4:pyre.caltech.edu")
    assert address.family == ipv4.family
    assert address.host == "pyre.caltech.edu"
    assert address.port == 0
    assert address.value == ("pyre.caltech.edu", 0)

    # ip4 with no family or port
    address = parser.parse("pyre.caltech.edu")
    assert address.family == ipv4.family
    assert address.host == "pyre.caltech.edu"
    assert address.port == 0
    assert address.value == ("pyre.caltech.edu", 0)

    # unix
    address = parser.parse("unix:/tmp/.s.5394")
    assert address.family == unix.family
    assert address.path == "/tmp/.s.5394"
    assert address.value == "/tmp/.s.5394"
    
    address = parser.parse("local:/tmp/.s.5394")
    assert address.family == unix.family
    assert address.path == "/tmp/.s.5394"
    assert address.value == "/tmp/.s.5394"
    
    return


# main
if __name__ == "__main__":
    test()


# end of file 
