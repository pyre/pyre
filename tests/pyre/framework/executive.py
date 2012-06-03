#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the executive can be instantiated
"""


def test():
    import pyre.framework
    executive = pyre.framework.executive(managers=pyre.framework)
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
