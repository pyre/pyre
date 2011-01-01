#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the configuration factory is accessible
"""


def test():
    import pyre.config
    return pyre.config.newConfiguration()


# main
if __name__ == "__main__":
    test()


# end of file 
