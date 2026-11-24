#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a block inside a block of the backup server is written as a savepoint
"""


def test():
    """
    Nest two blocks around an insert, and check the script the backup server writes
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        # the key
        id = pyre.db.int().primary()
        # and the word
        text = pyre.db.str()

    # support
    import io

    # a stream to write into
    stream = io.StringIO()
    # and a server that writes into it
    db = pyre.db.backup(name="nested", stream=stream).attach()
    # a transaction
    with db:
        # with a block inside it
        with db:
            # that adds a word
            db.insert(Word.pyre_immutable(id=1, text="nested"))
    # the script
    lines = [line for line in stream.getvalue().splitlines() if line]
    # opens the transaction, sets a savepoint, inserts, releases it, and commits
    assert lines == [
        "START TRANSACTION;",
        "SAVEPOINT pyre_1;",
        "INSERT INTO words",
        "    (id, text)",
        "  VALUES",
        "    (1, 'nested');",
        "RELEASE SAVEPOINT pyre_1;",
        "COMMIT;",
    ], lines
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
