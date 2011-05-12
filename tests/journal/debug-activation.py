#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that debug channels by the same name share a common state
"""


def test():
    # access the package
    import journal
    # build a debug channel
    debug = journal.debug("activation")
    # verify that it is on by default, activated from a configuration source
    assert debug.active == True
    # enable it
    debug.active = False

    # access the same channel through another object
    clone = journal.debug("activation")
    # verify that it is now on
    assert clone.active == False

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
