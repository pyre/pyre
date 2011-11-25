#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify the selector can raise alarms
"""


def test():
    # if necessary
    # import journal
    # journal.debug("pyre.ipc.selector").active = True
    # access the package
    import pyre.ipc
    # instantiate a selector
    s = pyre.ipc.selector()
    
    # get time
    from time import time as now
    # get the units of time
    from pyre.units.SI import second
    # build a counter
    import itertools
    counter = itertools.count()
    # build a handler
    def handler(scheduler, timestamp):
        n = next(counter)
        # print("n={}, time={}".format(n, timestamp))
        return

    # setup some alarms
    s.alarm(interval=0, handler=handler)
    s.alarm(interval=1*second, handler=handler)
    s.alarm(interval=0.5*second, handler=handler)
    s.alarm(interval=0.25*second, handler=handler)
    s.alarm(interval=0.75*second, handler=handler)
    s.alarm(interval=0.3*second, handler=handler)
    s.alarm(interval=0.5*second, handler=handler)
    # how many?
    alarms = len(s._alarms)

    # invoke the selector
    s.watch()
    # verify that all alarms fired
    assert next(counter) == alarms

    # and return the selector
    return s


# main
if __name__ == "__main__":
    test()


# end of file 
