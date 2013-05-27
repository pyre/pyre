#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Instantiate a simple mutable record using the keyword form
"""


def test():
    import pyre.records

    class record(pyre.records.record):
        """
        A sample record
        """
        sku = pyre.records.field()
        description = pyre.records.field()
        cost = pyre.records.field()


    # build a record
    r = record(sku="9-4013", description="organic kiwi", cost=.85)
    # check
    assert r.sku == "9-4013"
    assert r.description == "organic kiwi"
    assert r.cost == .85

    # make a change to the cost
    r.cost = 1

    # and verify that it was stored
    assert r.cost == 1

    # all done
    return r


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
