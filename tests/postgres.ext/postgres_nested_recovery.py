#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a failed statement inside a block does not abandon the transaction around it
"""


def test():
    """
    Fail a statement inside a block, and check that the transaction carries on
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="pyre_nested_recovery"):
        """
        Words
        """

        # the key
        id = pyre.db.int().primary()
        # and the word
        text = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="savepoints").attach()
    # make the table, outside any block, so it survives them
    db.createTable(Word)
    # carefully
    try:
        # and its exceptions
        from pyre.db import exceptions

        # work in a transaction
        with db:
            # keep one word
            db.insert(Word.pyre_immutable(id=1, text="kept"))
            # attempt to
            try:
                # work in a block inside it
                with db:
                    # with a statement that fails
                    db.execute("SELECT 1/0")
            # absorb the failure
            except exceptions.DataError:
                # and carry on with the transaction, which the savepoint saved
                pass
            # add another word, which postgres accepts only if the transaction survived
            db.insert(Word.pyre_immutable(id=2, text="after"))
        # read the table back
        words = sorted(row.text for row in db.select(Word))
        # both words were kept
        assert words == ["after", "kept"], words
    # either way
    finally:
        # leave nothing behind
        db.execute("DROP TABLE pyre_nested_recovery")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
