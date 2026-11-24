#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a block inside a transaction that fails undoes only its own work
"""


def test():
    """
    Fail a block inside a transaction, and check that the work of the transaction is kept
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        # the key
        id = pyre.db.int().primary()
        # and the word
        text = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="nested").attach()
    # make the table
    db.createTable(Word)
    # work in a transaction
    with db:
        # keep one word
        db.insert(Word.pyre_immutable(id=1, text="kept"))
        # attempt to
        try:
            # work in a block inside it
            with db:
                # add another word
                db.insert(Word.pyre_immutable(id=2, text="undone"))
                # and give up on the block
                raise ValueError("give up")
        # absorb the failure of the inner block
        except ValueError:
            # and carry on with the transaction
            pass
    # read the table back
    words = sorted(row.text for row in db.select(Word))
    # the outer word was kept, and the inner one undone
    assert words == ["kept"], words
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
