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
    # import journal
    # journal.debug("postgres.init").active = True
    # journal.debug("postgres.connection").active = True
    # journal.debug("postgres.execution").active = True

    from postgres import postgres as pyrepg
    # initialize the module exceptions
    import pyre.db.exceptions as exceptions
    pyrepg.registerExceptions(exceptions)

    # make a connection
    connection = pyrepg.connect("dbname=pyre")
    # execute a command
    command = "SELECT datname FROM pg_database WHERE datname='pyre'"
    # submit it for asynchronous processing
    pyrepg.submit(connection, command)

    # loop until the entire result has been assembled
    while pyrepg.busy(connection):
        pyrepg.consume(connection)

    # retrieve it
    result = pyrepg.retrieve(connection)
    # check that we got what we expected
    assert result == (('datname',), ('pyre',))

    # call retrieve again; this time there should be nothing to get
    result = pyrepg.retrieve(connection)
    assert result == None

    # and return the connection and the resulting tuple
    return connection, result


# main
if __name__ == "__main__":
    test()


# end of file 
