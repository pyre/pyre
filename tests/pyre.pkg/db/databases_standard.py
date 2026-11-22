#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the standard mill refuses to create or drop a database, which standard SQL has no
statements for
"""


def test():
    """
    Ask the standard mill for the statements that create and drop a database
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="databases_standard")

    # go through the requests
    for request in (mill.createDatabase, mill.dropDatabase):
        # attempt to
        try:
            # build the statement
            statement = tuple(request(name="inventory"))
        # which must fail
        except exceptions.NotSupportedError as error:
            # naming the language
            assert "standard SQL" in str(error), str(error)
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
