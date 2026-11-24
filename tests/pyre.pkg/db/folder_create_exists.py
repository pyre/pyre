#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server refuses to make a table that is there already, unless it is told that
finding it there is fine, and then leaves its rows alone
"""


def test():
    """
    Make a table, add a row, and make it again, with and without {existOk}
    """
    # externals
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

    # the folder, named after this driver and kept for inspection
    folder = "folder_create_exists"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_create_exists", path=folder).attach()
    # make the table
    db.createTable(Granule)
    # with a granule
    db.load(Granule.pyre_immutable(name="a"))
    # carefully
    try:
        # make it again
        db.createTable(Granule)
    # it must be refused
    except pyre.db.exceptions.ProgrammingError as error:
        # naming the table
        assert "granules" in str(error), str(error)
    # if it is not
    else:
        # say so
        assert False, "a table that is there already was made again"
    # finding it there is fine when the caller says so
    db.createTable(Granule, existOk=True)
    # and its rows are still there
    assert [row.name for row in db.select(query=Granule)] == ["a"]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
