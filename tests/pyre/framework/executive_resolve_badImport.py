#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that bad component descriptors raise the correct exceptions
"""


def test():
    import pyre.framework
    executive = pyre.framework.executive()

    # attempt to retrieve a non-existent component descriptor from the python path
    try:
        unkown, = executive.resolve(uri="import:not-there/unknown")
        assert False
    except ValueError:
        pass
    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
