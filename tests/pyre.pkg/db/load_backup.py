#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a backup server writes a load as the inserts of its records, in one transaction
"""


def test():
    """
    Load two words through a backup server, and read what it wrote
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
    path = "load_backup.sql"
    # make a server that writes there
    db = pyre.db.backup(name="backup", stream=path)
    # connect it
    db.attach()
    # load two words
    db.load(Word.pyre_immutable(text="one"), Word.pyre_immutable(text="two"))
    # make sure everything is on disk
    db.stream.close()
    # read what was written
    with open(path) as stream:
        # all of it
        statements = stream.read().strip()
    # the load is one transaction, which opens
    assert statements.startswith("START TRANSACTION"), statements
    # and commits
    assert statements.endswith("COMMIT;"), statements
    # and in between, inserts into the table
    assert "INSERT INTO words" in statements, statements
    # both words
    assert "'one'" in statements and "'two'" in statements, statements
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
