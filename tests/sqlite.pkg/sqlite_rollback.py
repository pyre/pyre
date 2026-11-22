#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a transaction block that raises leaves nothing behind
"""


def test():
    """
    Insert a word in a transaction block that raises, and look for it
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        """
        Words
        """

        # the word
        text = pyre.db.str()

    # the condition the block raises
    class Abandoned(Exception):
        """
        Exception raised when the block gives up on its transaction
        """

    # connect to a database in memory
    db = pyre.db.sqlite(name="rollback").attach()
    # make the table
    db.createTable(Word)
    # attempt to
    try:
        # in a transaction
        with db:
            # put a word in the table
            db.insert(Word.pyre_immutable(text="lost"))
            # and give up
            raise Abandoned()
    # when the block gives up
    except Abandoned:
        # there is nothing more to do
        pass
    # the word is not there
    words = [row.text for row in db.select(Word)]
    # so check
    assert words == [], words
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
