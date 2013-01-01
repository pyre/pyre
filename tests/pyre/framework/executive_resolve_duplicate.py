#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify that the binder can retrieve components from odb files
"""


def test():
    import pyre.framework
    executive =  pyre.framework.executive()

    # retrieve a component descriptor from a file
    one, = executive.resolve(uri="file:sample.odb/one")
    two, = executive.resolve(uri="file:sample.odb/one")
    # check that the two retrievals yield identical results
    assert one == two

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
