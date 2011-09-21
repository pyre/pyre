#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the configurator factory is accessible
"""


def test():
    # access the package
    import pyre
    # and return the configurator built by the executive
    return pyre.executive.configurator


# main
if __name__ == "__main__":
    test()


# end of file 
