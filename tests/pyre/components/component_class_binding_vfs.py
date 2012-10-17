#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that facilities get bound correctly when specified implicitly
"""


def test():
    import pyre

    # declare a protocol
    class task(pyre.protocol, family='a.very.long.family.name'):
        """a protocol"""
        @pyre.provides
        def do(self):
            """do something"""

    # declare a component
    class worker(pyre.component):
        """a component"""
        # job = task(default="vfs:/pyre/startup/sample.py/relax")
        job = task(default="sample.py/relax")

    # check that task was bound according to our expectations from sample.py
    assert issubclass(worker.job, pyre.component)
    assert worker.job.__name__ == "relax"
    assert task.pyre_isCompatible(worker.job)

    return worker, task


# main
if __name__ == "__main__":
    test()


# end of file 
