#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the updates of one call are all or nothing
"""


def test():
    """
    Update two words in one call, the second of which fails, and check neither changed
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="pyre_update_atomic"):
        """
        Words
        """

        # the key
        id = pyre.db.int().primary()
        # and the word
        text = pyre.db.str()

    # a word is never empty
    Word.pyre_check(Word.text != "")

    # connect
    db = pyre.db.postgres(name="savepoints").attach()
    # make the table, outside any block, so it survives them
    db.createTable(Word)
    # carefully
    try:
        # and its exceptions
        from pyre.db import exceptions

        # with two words
        db.insert(Word.pyre_immutable(id=1, text="one"), Word.pyre_immutable(id=2, text="two"))
        # attempt to
        try:
            # rename the first, and empty the second, which the check refuses
            db.update(
                (Word.pyre_immutable(text="renamed"), Word.id == 1),
                (Word.pyre_immutable(text=""), Word.id == 2),
            )
        # which fails
        except exceptions.IntegrityError:
            # as it must
            pass
        # read the table back
        words = sorted(row.text for row in db.select(Word))
        # neither word changed: the two updates were all or nothing
        assert words == ["one", "two"], words
    # either way
    finally:
        # leave nothing behind
        db.execute("DROP TABLE pyre_update_atomic")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
