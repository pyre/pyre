#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the trait defaults get bound correctly
"""


def test():
    import pyre

    # declare an interface
    class job(pyre.interface):
        """an interface"""
        @pyre.provides
        def do(self):
            """do something"""

    # declare a component the implements this interface
    class worker(pyre.component, implements=job):
        """an implementation"""
        @pyre.export
        def do(self):
            """do something"""

    # declare a component
    class base(pyre.component):
        """the base component"""
        number = pyre.properties.int(default=1)
        task = pyre.facility(interface=job, default=worker)

    # check the default values
    assert base.number == 1
    assert base.task == worker

    return base


# main
if __name__ == "__main__":
    test()


# end of file 
