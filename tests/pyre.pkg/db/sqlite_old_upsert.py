#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of an sqlite too old for ON CONFLICT refuses to keep or replace rows,
naming both versions
"""


def test():
    """
    Ask the dialect of an sqlite before 3.24 to replace the rows that are there already, and
    check it refuses
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # the dialect of an sqlite that predates ON CONFLICT
    class Old(pyre.db.backends.sqlite.mill):
        """
        The dialect of sqlite 3.22.0
        """

        # the version of the library
        version = (3, 22, 0)

    # make one
    mill = Old(name="old")
    # attempt to
    try:
        # build the statement
        statement = tuple(
            mill.insertRecords(Granule.pyre_immutable(id=1, name="first"), existing="replace")
        )
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the version it has and the one it needs
        assert "sqlite 3.22.0" in str(error) and "3.24" in str(error), str(error)
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
