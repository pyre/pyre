#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of postgres refuses to create a database only when it is missing,
which postgres has no statement for
"""


def test():
    """
    Ask the dialect of postgres to create a database that may exist, and check it refuses
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # make a mill
    mill = pyre.db.backends.postgres.mill(name="refusal")
    # attempt to
    try:
        # build the statement
        statement = tuple(mill.createDatabase(name="inventory", existOk=True))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming what it was asked for
        assert "the database inventory" in str(error), str(error)
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
