#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Access timers through the pyre executive
"""


def test():
    # access
    import pyre

    # make one
    t = pyre.executive.timer(name="test")

    # start it
    t.start()
    # stop it 
    t.stop()
    assert t._accumulatedTime != 0
    # read it
    t.read()

    # start it again
    t.start()
    # take a lap reading
    t.lap()
    # stop it
    t.stop()

    # reset it
    t.reset()
    assert t._accumulatedTime == 0
    
    return t


# main
if __name__ == "__main__":
    test()


# end of file 
