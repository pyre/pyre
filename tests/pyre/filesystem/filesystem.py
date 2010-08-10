#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that we can create filesystem instances
"""


def test():
    from pyre.filesystem.Filesystem import Filesystem
    return Filesystem()


# main
if __name__ == "__main__":
    test()


# end of file 
