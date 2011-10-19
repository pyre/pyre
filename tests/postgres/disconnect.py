#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Open a connection and close it explicitly
"""


def test():
    # import the postgres module
    import postgres
    # use the high level connection factory
    connection = postgres.connect(database='postgres', application='connect')
    # and shut it down explicitly
    connection.close()
    # return the connection
    return connection


# main
if __name__ == "__main__":
    test()


# end of file 
