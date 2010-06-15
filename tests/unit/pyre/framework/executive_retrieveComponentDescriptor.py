#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the binder can retrieve components from odb files
"""


def test():
    import pyre.framework
    executive =  pyre.framework.executive()

    # retrieve a component descriptor from the puthon path
    base = executive.retrieveComponentDescriptor(uri="import://pyre.components.Component#Component")
    print(base)
    # retrieve a component descriptor from a file
    one = executive.retrieveComponentDescriptor(uri="file://local/sample.odb#one")
    print(one)
    # check that one derives from the other
    assert issubclass(one, base)

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
