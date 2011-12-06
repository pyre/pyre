#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the package manager is accessible
"""


def test():
    # access to the merlin executive
    from merlin import merlin

    # get the curator
    packages = merlin.packages

    # check the name
    assert packages

    # and return
    return packages


# main
if __name__ == "__main__":
    test()


# end of file 
