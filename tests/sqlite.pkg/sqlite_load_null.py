#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a load stores the values a record leaves missing as NULL
"""


def test():
    """
    Load a record with a missing value next to one without, and read them back
    """
    # access the package
    import pyre.db

    # a table of notes
    class Note(pyre.db.table, id="notes"):
        """
        Notes
        """

        # the key
        id = pyre.db.int().primary()
        # and the text
        text = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="load_null").attach()
    # make the table
    db.createTable(Note)
    # load a note with text and one without
    db.load(Note.pyre_immutable(id=1, text="hello"), Note.pyre_immutable(id=2, text=None))
    # read them back, in order
    rows = sorted(db.select(Note), key=lambda row: row.id)
    # the missing text is NULL
    assert [row.text for row in rows] == ["hello", None], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
