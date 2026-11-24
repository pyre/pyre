#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a transaction block of a folder server that raises leaves the folder as it found it:
the tables the block made are gone, and so are the rows it added to the others
"""


def test():
    """
    In a block that raises, add rows to one table and make another, then look at the folder
    """
    # externals
    import os
    import shutil

    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # and one of notes
    class Note(pyre.db.table, id="notes"):
        """
        Notes
        """

        # the text
        text = pyre.db.str()

    # the exception that ends the block
    class Stop(Exception):
        """
        Exception raised to end the transaction block
        """

    # the folder, named after this driver and kept for inspection
    folder = "folder_rollback"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_rollback", path=folder).attach()
    # make the table of granules
    db.createTable(Granule)
    # with a granule
    db.load(Granule.pyre_immutable(name="a"))
    # whether the block ended
    stopped = False
    # carefully
    try:
        # in a transaction block
        with db:
            # add a granule
            db.load(Granule.pyre_immutable(name="b"))
            # make the table of notes
            db.createTable(Note)
            # with a note
            db.load(Note.pyre_immutable(text="seen"))
            # and end the block
            raise Stop()
    # the end of the block
    except Stop:
        # is what is expected
        stopped = True
    # make sure it happened
    assert stopped
    # the table of notes is gone
    assert os.listdir(folder) == ["granules.tsv"], os.listdir(folder)
    # and the granules are the ones that were there before the block
    assert [row.name for row in db.select(query=Granule)] == ["a"]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
