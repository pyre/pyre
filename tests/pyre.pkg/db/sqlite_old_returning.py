#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of an sqlite too old for RETURNING refuses it, naming both versions
"""


def test():
    """
    Ask the dialect of an sqlite before 3.35 for the rows a deletion removes, and check it
    refuses
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()

    # the dialect of an sqlite that predates RETURNING
    class Old(pyre.db.backends.sqlite.mill):
        """
        The dialect of sqlite 3.31.1
        """

        # the version of the library
        version = (3, 31, 1)

    # make one
    mill = Old(name="old")
    # attempt to
    try:
        # build the statement
        statement = tuple(
            mill.deleteRecords(table=Granule, condition=Granule.id == 1, returning=Granule)
        )
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the version it has and the one it needs
        assert "sqlite 3.31.1" in str(error) and "3.35" in str(error), str(error)
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
