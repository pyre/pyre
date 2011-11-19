#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the selector factory is accessible
"""


def test():
    # access the package
    import pyre.ipc
    # instantiate a selector
    s = pyre.ipc.selector()
    # and return it
    return s


# main
if __name__ == "__main__":
    test()


# end of file 
