#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that postgres stores json documents and reads them back, as documents or as text, and
refuses a document whose top level is text unless it is read as text
"""


def test():
    """
    Store documents, and read them back in each of the ways a column allows
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of documents
    class Documents(pyre.db.table, id="pyre_json"):
        # the key
        id = pyre.db.int().primary()
        # the document
        doc = pyre.db.json()

    # the same table, read as text
    class Texts(pyre.db.table, id="pyre_json"):
        # the key
        id = pyre.db.int().primary()
        # the document, read as its text
        doc = pyre.db.json().asText()

    # connect
    db = pyre.db.postgres(name="json").attach()
    # make the table
    db.createTable(Documents)
    # carefully
    try:
        # store a document
        db.insert(Documents.pyre_immutable(id=1, doc={"a": [1, 2.5, None, True]}))
        # read it back
        (row,) = db.select(Documents)
        # as a document
        assert row.doc == {"a": [1, 2.5, None, True]}, row.doc
        # and as its text
        (row,) = db.select(Texts)
        # which is the canonical text of the document
        assert row.doc == '{"a": [1, 2.5, null, true]}', row.doc
        # store a document whose top level is text
        db.execute("INSERT INTO pyre_json (id, doc) VALUES (2, '\"just text\"')")
        # reading it as a document
        try:
            # must fail
            list(db.select(Documents))
        # naming the column
        except exceptions.DataError as error:
            # in its explanation
            assert "doc" in str(error), str(error)
        # if it doesn't
        else:
            # complain
            assert False, "a document whose top level is text was read as a document"
        # while reading it as text works
        texts = {row.id: row.doc for row in db.select(Texts)}
        # and gives its text
        assert texts[2] == '"just text"', texts
    # either way
    finally:
        # leave nothing behind
        db.execute("DROP TABLE pyre_json")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
