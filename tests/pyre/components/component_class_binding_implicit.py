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
        task = pyre.facility(interface=job, default="import://sample#worker")

    # check that task was bound according to our expectations from sample.py
    assert issubclass(component.task, pyre.component)
    assert component.task.pyre_name == "worker"
    assert job.pyre_isCompatible(component.task)

    return component, job


# main
if __name__ == "__main__":
    test()


# end of file 
