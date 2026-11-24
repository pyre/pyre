#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a load carries text that holds the characters the format of a copy escapes, the tab,
the newline, the carriage return and the backslash, as it was given
"""


def test():
    """
    Load text with each of the characters a copy escapes, and read it back
    """
    # access the package
    import pyre.db

    # a table of notes
    class Note(pyre.db.table, id="pyre_load_text"):
        """
        Notes
        """

        # the key
        id = pyre.db.int().primary()
        # and the text
        text = pyre.db.str()

    # the awkward text
    texts = ["a\tb", "c\nd", "e\rf", "g\\h", "\\N"]

    # connect
    db = pyre.db.postgres(name="load_text").attach()
    # make the table
    db.createTable(Note)
    # carefully
    try:
        # load the notes
        db.load(*(Note.pyre_immutable(id=index, text=text) for index, text in enumerate(texts)))
        # read them back, in order
        rows = sorted(db.select(Note), key=lambda row: row.id)
        # the text came back as it was given
        assert [row.text for row in rows] == texts, rows
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Note)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
