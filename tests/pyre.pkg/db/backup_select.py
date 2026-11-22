#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection through a backup server writes its statement and yields no rows
"""


def test():
    """
    Select the rows of a table through a backup server
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
    path = "backup_select.sql"
    # make a server that writes there
    db = pyre.db.backup(name="backup_select", stream=path)
    # select the words
    rows = list(db.select(Word))
    # there are none, since a backup only writes
    assert rows == [], rows
    # make sure everything is on disk
    db.stream.close()
    # read what was written
    with open(path) as stream:
        # all of it
        statements = stream.read().strip()
    # it is the selection
    assert statements.startswith("SELECT"), statements
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
