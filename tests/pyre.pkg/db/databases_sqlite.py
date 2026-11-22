#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of sqlite refuses to create or drop a database, since a sqlite database
is the file it is attached to
"""


def test():
    """
    Ask the dialect of sqlite for the statements that create and drop a database
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.dialects.sqlite(name="databases_sqlite")

    # go through the requests
    for request in (mill.createDatabase, mill.dropDatabase):
        # attempt to
        try:
            # build the statement
            statement = tuple(request(name="inventory"))
        # which must fail
        except exceptions.NotSupportedError as error:
            # naming the language
            assert "sqlite" in str(error), str(error)
            # and the database
            assert "inventory" in str(error), str(error)
        # if it doesn't
        else:
            # the statement was built anyway
            assert False, statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
