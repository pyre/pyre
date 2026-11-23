#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses a column of json documents, which it has no type for
"""


def test():
    """
    Declare a table with a column of json documents, and check the standard mill refuses it
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of documents
    class Documents(pyre.db.table, id="documents"):
        # the document
        doc = pyre.db.json()

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="columns_json_standard")
    # attempt to
    try:
        # build the statement that creates the table
        statement = tuple(mill.createTable(table=Documents))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the column
        assert error.column == "doc", error.column
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
