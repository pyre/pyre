#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a database another connection holds is reported as an operational error, once the
wait for it runs out
"""


def test():
    """
    Hold a database in one connection, write to it from another, and check the refusal
    """
    # access the package
    import pyre.db

    # a file both connections reach, named after me and left behind
    path = "sqlite_error_busy.sql"

    # a table of notes
    class Note(pyre.db.table, id="notes"):
        # the text
        text = pyre.db.str()

    # one connection
    holder = pyre.db.sqlite(name="holder", database=path).attach()
    # makes the table, unless an earlier run did
    holder.createTable(Note, existOk=True)
    # and holds the database
    holder.execute("BEGIN EXCLUSIVE;")
    # the other connection
    writer = pyre.db.sqlite(name="writer", database=path).attach()
    # attempts to
    try:
        # write to it
        writer.insert(Note.pyre_immutable(text="busy"))
    # which is refused, once the wait runs out
    except pyre.db.exceptions.OperationalError as error:
        # with sqlite's own name for the condition
        assert error.code == "SQLITE_BUSY", error.code
    # anything else
    else:
        # is a failure
        assert False, "the write was not refused"
    # let go of the database
    holder.execute("ROLLBACK;")
    # disconnect the writer
    writer.detach()
    # and the holder
    holder.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
