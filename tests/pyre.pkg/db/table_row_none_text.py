#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a row of a table keeps text that reads like the name of nothing
"""


def test():
    """
    Build rows of a table whose text is "None", and one with no text at all
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

    # a word that reads like the name of nothing
    word = Word.pyre_immutable(id=1, text="None")
    # stays text
    assert word.text == "None", word.text
    # and so does its lower case
    assert Word.pyre_immutable(id=2, text="none").text == "none"
    # while the absence of a word
    nothing = Word.pyre_immutable(id=3, text=None)
    # is still {None}
    assert nothing.text is None, nothing.text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
