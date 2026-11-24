#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a load is all or nothing: a record the server refuses undoes the ones before it
"""


def test():
    """
    Load records the last of which repeats a key, and check that the table is empty
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="pyre_load_atomic"):
        """
        Words
        """

        # the key
        id = pyre.db.int().primary()
        # and the word, which has a default, so the last record travels apart from the others
        text = pyre.db.str(default="word")

    # connect
    db = pyre.db.postgres(name="load_atomic").attach()
    # make the table
    db.createTable(Word)
    # carefully
    try:
        # attempt to
        try:
            # load two words, and a third that repeats the key of the first
            db.load(
                Word.pyre_immutable(id=1, text="one"),
                Word.pyre_immutable(id=2, text="two"),
                Word.pyre_immutable(id=1, text=Word.default),
            )
        # which is refused
        except pyre.db.exceptions.IntegrityError:
            # and nothing was kept
            assert list(db.select(Word)) == []
        # anything else
        else:
            # is a failure
            assert False, "a repeated key was accepted"
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Word)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
