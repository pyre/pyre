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
    try:
        executive.retrieveComponentDescriptor(uri="import://not-there#unknown")
        assert False
    except executive.DecodingError as error:
        pass
    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
