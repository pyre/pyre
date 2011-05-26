#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the binder can retrieve components from odb files
"""


def test():
    import pyre.framework
    executive = pyre.framework.executive()

    # retrieve a component descriptor from the python path
    base = executive.retrieveComponentDescriptor(uri="import:pyre.component")
    # retrieve a component descriptor from a file using the virtual filesystem
    d1 = executive.retrieveComponentDescriptor(uri="vfs:/local/sample.py/d1")
    # check that one derives from the other
    assert issubclass(d1, base)
    # retrieve a component descriptor from a file using the physical filesystem
    d2 = executive.retrieveComponentDescriptor(uri="file:sample.py/d2")
    # check that one derives from the other
    assert issubclass(d2, base)

    # exercise retrieving component instances
    a_d1 = executive.retrieveComponentDescriptor(uri="vfs:/local/sample.py/d1#a_d1")
    # check that it is an instance of d1
    # they are related since they come from the same shelf...
    assert isinstance(a_d1, d1)
    # and verify that the name is correct
    assert a_d1.pyre_name == "a_d1"

    # repeat with d2
    a_d2 = executive.retrieveComponentDescriptor(uri="file:sample.py/d2#a_d2")
    # check that it is an instance of d2
    # they are related since they come from the same shelf...
    assert isinstance(a_d2, d2)
    # and verify that the name is correct
    assert a_d2.pyre_name == "a_d2"

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
