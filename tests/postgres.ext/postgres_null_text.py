#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the text {None} reads back as itself, and not as NULL
"""


def test():
    """
    Store the words None and none, and read them back
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="pyre_null_text"):
        """
        Words, some of which look like python's name for nothing
        """

        # the key
        id = pyre.db.int().primary()
        # the word
        text = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="nulls").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Word)
        # store the words
        db.insert(Word.pyre_immutable(id=1, text="None"), Word.pyre_immutable(id=2, text="none"))
        # read them back
        words = {row.id: row.text for row in db.select(Word)}
        # they must be the words, not the absence of one
        assert words == {1: "None", 2: "none"}, words
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
