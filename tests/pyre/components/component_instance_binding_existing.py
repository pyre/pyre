#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that facilities get bound correctly to existing instances
"""


def test():
    import pyre

    # declare an interface
    class job(pyre.interface):
        """an interface"""
        @pyre.provides
        def do(self):
            """do something"""

    # declare a component
    class component(pyre.component):
        """a component"""
        w1 = pyre.facility(interface=job)
        w2 = pyre.facility(interface=job)

    # instantiate
    c = component(name="c")
    # bind {w1} and {w2}
    c.w1 = "import:sample.worker#worker"
    c.w2 = "import:sample.worker#worker"
    # check
    assert c.w1 is c.w2
    assert c.w1.pyre_name == 'worker'

    return c, component, job


# main
if __name__ == "__main__":
    test()


# end of file 
