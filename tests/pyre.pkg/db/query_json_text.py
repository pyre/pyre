#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of postgres reads a column of json documents as text when asked to
"""


def test():
    """
    Render the selection of a table whose document is read as text
    """
    # access the package
    import pyre.db

    # a table of documents
    class Documents(pyre.db.table, id="documents"):
        # the key
        id = pyre.db.int().primary()
        # the document, read as its text
        doc = pyre.db.json().asText()

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="query_json_text")
    # generate the statement
    statement = tuple(mill.select(Documents))
    # and check it
    assert statement == (
        "SELECT",
        "    id,",
        "    doc::text AS doc",
        "  FROM documents;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
