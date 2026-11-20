#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the statements a backup server writes inside a transaction block are bracketed by
the statements that make them one transaction
"""


def test():
    """
    Write a table and a row through a backup server, in a transaction block
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        """
        Words
        """

        # the word
        text = pyre.db.str()

    # the file the statements go to, named after this driver and kept for inspection
    path = "backup_transaction.sql"
    # make a server that writes there
    db = pyre.db.backup(name="backup", stream=path)
    # connect it
    db.attach()
    # in a transaction
    with db:
        # make the table
        db.createTable(Word)
        # and put a word in it
        db.insert(Word.pyre_immutable(text="kept"))
    # make sure everything is on disk
    db.stream.close()
    # read what was written
    with open(path) as stream:
        # all of it
        statements = stream.read().strip()
    # it opens a transaction
    assert statements.startswith("START TRANSACTION"), statements
    # and commits it
    assert statements.endswith("COMMIT;"), statements
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
