#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: make sure we can instantiate variable slots
"""

def test():
    # for the locator
    import pyre.tracking
    # get the slot class
    from pyre.framework.Slot import Slot

    # make a value
    value = 4
    # build a locator and a priority
    key = None
    locator = pyre.tracking.here()
    priority = Slot.priorities.explicit()
    
    # make a slot
    return Slot.variable(key=key, value=value, locator=locator, priority=priority)


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
