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
    executive =  pyre.framework.executive()

    # retrieve a component descriptor from the python path
    base = executive.retrieveComponentDescriptor(uri="import:pyre.components.Component#Component")
    # retrieve a component descriptor from a file using the virtual filesystem
    one = executive.retrieveComponentDescriptor(uri="vfs:///local/sample.odb#one")
    # check that one derives from the other
    assert issubclass(one, base)
    # retrieve a component descriptor from a file using the physical filesystem
    two = executive.retrieveComponentDescriptor(uri="file:sample.odb#two")
    # check that one derives from the other
    assert issubclass(two, base)
    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
