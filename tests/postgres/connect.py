#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Make a connection through the high level interface
"""


def test():
    # import the postgres module
    import postgres
    # use the high level connection factory
    connection = postgres.connect(database='pyrepg', application='connect')
    # return the connection
    return connection


# main
if __name__ == "__main__":
    test()


# end of file 
