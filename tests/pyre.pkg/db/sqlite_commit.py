#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that what a transaction on a sqlite database does is still there after detaching
"""


def test():
    """
    Insert a row in a transaction, detach, attach again, and look for it
    """
    # support
    import os

    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        """
        Words
        """

        # the word
        text = pyre.db.str()

    # the database file, named after this driver and kept for inspection
    path = "sqlite_commit.db"
    # start from scratch
    if os.path.exists(path):
        # by removing what an earlier run left
        os.remove(path)
    # connect
    db = pyre.db.sqlite(name="commit", database=path).attach()
    # in a transaction
    with db:
        # make the table
        db.createTable(Word)
        # and put a word in it
        db.insert(Word.pyre_immutable(text="kept"))
    # let go
    db.detach()
    # connect again
    db.attach()
    # the word is still there
    words = [row.text for row in db.select(Word)]
    # so check
    assert words == ["kept"], words
    # let go
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
