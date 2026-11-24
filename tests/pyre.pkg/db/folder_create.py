#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server makes its folder when it attaches, and a table as an empty file of
rows named after it
"""


def test():
    """
    Attach a folder server, make a table, and look at the folder
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

    # the folder, named after this driver and kept for inspection
    folder = "folder_create"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_create", path=folder).attach()
    # which makes it
    assert os.path.isdir(folder)
    # make the table
    db.createTable(Granule)
    # which is an empty file named after it
    assert os.listdir(folder) == ["granules.tsv"], os.listdir(folder)
    # with no rows
    assert os.path.getsize(os.path.join(folder, "granules.tsv")) == 0
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
