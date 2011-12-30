#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the command line parser can be instantiated
"""


def test():
    import pyre.config
    return pyre.config.newCommandLineParser()


# main
if __name__ == "__main__":
    test()


# end of file 
