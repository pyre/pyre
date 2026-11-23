#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the types the dialect of postgres declares for columns of json documents
"""


def test():
    """
    Declare a column of json documents, and one that keeps their text as written
    """
    # access the package
    import pyre.db

    # a table of documents
    class Documents(pyre.db.table, id="documents"):
        # a document, in the binary form postgres prefers
        doc = pyre.db.json()
        # and one whose text is kept as it was written
        raw = pyre.db.json().verbatim()

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="columns_json_postgres")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Documents))
    # and check it
    assert statement == (
        "CREATE TABLE documents (",
        "  doc JSONB,",
        "  raw JSON",
        ");",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
