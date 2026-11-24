#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server reads every escape of the text format of postgres's copies, including
the ones it never writes, so that it reads the files postgres writes
"""


def test():
    """
    Write the file of a table by hand, with every escape, and select its rows
    """
    # externals
    import shutil

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

    # the folder, named after this driver and kept for inspection
    folder = "folder_select_escapes"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_select_escapes", path=folder).attach()
    # make the table
    db.createTable(Note)
    # write its rows by hand
    with open(f"{folder}/notes.tsv", "w") as stream:
        # the escapes of the control characters
        print("1\t\\b\\f\\n\\r\\t\\v", file=stream)
        # an octal and a hex escape, an escaped backslash, and a character that stands for itself
        print("2\t\\101\\x42\\\\C\\D", file=stream)
        # and null
        print("3\t\\N", file=stream)
    # read the notes
    notes = [(row.id, row.text) for row in db.select(query=Note)]
    # and check them
    assert notes == [(1, "\b\f\n\r\t\v"), (2, "AB\\CD"), (3, None)], notes
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
