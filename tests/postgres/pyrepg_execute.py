#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Make a connection to a database using the low level interface from the extension module
"""


def test():
    from postgres import postgres as pyrepg
    # initialize the module exceptions
    import pyre.db.exceptions as exceptions
    pyrepg.registerExceptions(exceptions)

    # make a connection
    connection = pyrepg.connect("dbname=pyre")
    # execute a command
    command = "SELECT datname FROM pg_database WHERE datname='pyre'"
    result = pyrepg.execute(connection, command)
    # check that we got what we expected
    assert result == (('datname',), ('pyre',))

    # and return the connection and the resulting tuple
    return connection, result


# main
if __name__ == "__main__":
    test()


# end of file 
