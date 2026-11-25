#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the values of a statement travel beside it, so the settings of a session cannot
change what they say
"""


def test():
    """
    Turn backslashes into escapes after attaching, on a server that still can, write a value that
    would end its literal early, and read it back
    """
    # access the package
    import pyre.db

    # a table of notes
    class Note(pyre.db.table, id="pyre_parameters_notes"):
        # the text
        text = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="parameters").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # a server before postgres 19 may be told to read backslashes as escapes
        if db.connection.server < 190000:
            # so tell it to, from now on
            db.execute("SET LOCAL standard_conforming_strings = off")
        # make the table
        db.createTable(Note)
        # a value that carries a statement of its own past an escaped quote
        value = "\\'; SELECT 42 AS injected; --"
        # write it
        db.insert(Note.pyre_immutable(text=value))

        # a query of the notes that hold it
        class Found(pyre.db.query, note=Note):
            # the text
            text = note.text
            # the restriction
            where = note.text == value

        # read it back
        rows = [row.text for row in db.select(Found)]
        # it is the value we wrote
        assert rows == [value], rows
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
