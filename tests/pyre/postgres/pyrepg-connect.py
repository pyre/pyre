#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the module is accessible
"""


def test():
    from pyre.postgres import pyrepg
    # initialize the module exceptions
    import pyre.db.exceptions as exceptions
    pyrepg.registerExceptions(exceptions)

    # make a connection
    connection = pyrepg.connect("dbname=pyrepg")
    # and return it
    return connection


# main
if __name__ == "__main__":
    test()


# end of file 
