#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the standard mill refuses to declare a column of identifiers, which standard SQL has
no type for, and names the table and the column
"""


def test():
    """
    Declare a table with a column of identifiers, and check the standard mill refuses it
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table with a column of identifiers
    class Things(pyre.db.table, id="things"):
        # the identifier
        tag = pyre.db.uuid(default=None)

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="columns_standard_uuid")
    # attempt to
    try:
        # build the statement that creates the table
        statement = tuple(mill.createTable(table=Things))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the table
        assert error.table == "things", error.table
        # and the column
        assert error.column == "tag", error.column
        # in its explanation as well
        assert "things" in str(error) and "tag" in str(error), str(error)
    # if it doesn't
    else:
        # the column was declared anyway
        assert False, statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
