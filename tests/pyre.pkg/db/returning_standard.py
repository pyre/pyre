#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses to return the rows a statement changes
"""


def test():
    """
    Ask the standard mill for the rows a deletion removes, and check it refuses
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # and its exceptions
    from pyre.db import exceptions

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="returning")
    # attempt to
    try:
        # build the statement
        statement = tuple(
            mill.deleteRecords(table=Granule, condition=Granule.id == 2, returning=Granule)
        )
    # which must fail
    except exceptions.NotSupportedError as error:
        # saying what it was asked for
        assert "returns the rows" in str(error), str(error)
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
