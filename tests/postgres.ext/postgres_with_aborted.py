#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a transaction block whose transaction the server abandoned says that nothing was kept
"""


def test():
    """
    Make a statement fail inside a transaction block, swallow the error, and leave the block
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of words
    class Word(pyre.db.table, id="pyre_with_aborted"):
        """
        Words
        """

        # the word
        text = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="with_aborted").attach()
    # make the table, outside the block, so it survives it
    db.createTable(Word)
    # carefully
    try:
        # attempt to
        try:
            # work in a transaction
            with db:
                # put a word in the table
                db.insert(Word.pyre_immutable(text="lost"))
                # make a statement fail
                try:
                    # by dividing by zero
                    db.execute("SELECT 1/0")
                # and swallow the error, as careless code might
                except exceptions.DataError:
                    # by moving on
                    pass
        # leaving the block must say that the work was not kept
        except exceptions.OperationalError:
            # which is what we expect
            pass
        # otherwise
        else:
            # complain
            assert False, "the block of an abandoned transaction ended as if it had committed"
        # either way, the word is not there
        words = [row.text for row in db.select(Word)]
        # so check
        assert words == [], words
    # either way
    finally:
        # leave nothing behind
        db.execute("DROP TABLE pyre_with_aborted")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
