#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that facilities get bound correctly when specified implicitly
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
        task = pyre.facility(interface=job, default="import:sample#worker")

    # instantiate
    c = component(name="c")
    # check
    assert isinstance(c.task, pyre.component)
    assert c.task.pyre_name == "c.task"

    return c, component, job


# main
if __name__ == "__main__":
    test()


# end of file 
