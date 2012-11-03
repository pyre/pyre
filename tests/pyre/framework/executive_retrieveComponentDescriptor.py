#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that the binder can retrieve components from odb files
"""


def test():
    import pyre.framework
    executive = pyre.framework.executive()

    # retrieve a component descriptor from the python path
    bases = tuple(executive.retrieveComponentDescriptor(uri="import:pyre.component"))
    for base in bases: assert base is pyre.component
    # retrieve a component descriptor from a file using the virtual filesystem
    d1, = executive.retrieveComponentDescriptor(uri="vfs:/pyre/startup/sample.py/d1")
    # check that one derives from the other
    assert issubclass(d1, base)
    # retrieve a component descriptor from a file using the physical filesystem
    d2, = executive.retrieveComponentDescriptor(uri="file:sample.py/d2")
    # check that one derives from the other
    assert issubclass(d2, base)

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
