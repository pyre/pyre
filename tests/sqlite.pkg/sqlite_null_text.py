#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that sqlite stores and reads back text that reads like the name of nothing
"""


def test():
    """
    Store the words "None" and "none", and read them back
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        """
        Words, by number
        """

        # the key
        id = pyre.db.int().primary()
        # the word
        text = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="null_text").attach()
    # make the table
    db.createTable(Word)
    # store the words
    db.insert(Word.pyre_immutable(id=1, text="None"), Word.pyre_immutable(id=2, text="none"))
    # read them back
    words = {row.id: row.text for row in db.select(Word)}
    # they must be the words, not the absence of one
    assert words == {1: "None", 2: "none"}, words
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
