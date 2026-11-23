#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the literal the dialect of postgres writes for a json document
"""


def test():
    """
    Insert a row with a json document, and check the statement
    """
    # access the package
    import pyre.db

    # a table of documents
    class Documents(pyre.db.table, id="documents"):
        # the document
        doc = pyre.db.json()

    # a row with a document that holds a quote
    row = Documents.pyre_immutable(doc={"a": [1, 2.5, None, True], "b": "it's"})
    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="literals_json_postgres")
    # build the statement that inserts it
    statement = tuple(mill.insertRecords(row))
    # and check it
    assert statement == (
        "INSERT INTO documents",
        "    (doc)",
        "  VALUES",
        """    ('{"a": [1, 2.5, null, true], "b": "it''s"}');""",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
