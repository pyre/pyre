#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server refuses the statements of SQL, since a folder only holds rows, and with
them the operations that are made of statements, such as an update
"""


def test():
    """
    Ask a folder server to execute a statement and to update a table
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
        # and the size
        size = pyre.db.int()

    # the folder, named after this driver and kept for inspection
    folder = "folder_statements_refused"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_statements_refused", path=folder).attach()
    # make the table
    db.createTable(Granule)
    # the template of an update
    template = pyre.db.template(Granule)
    # that sets the size
    template.size = 1
    # the attempts
    attempts = (
        # a statement given as text
        lambda: db.execute("SELECT 1;"),
        # and an update
        lambda: db.update((template, Granule.name == "a")),
    )
    # go through them
    for attempt in attempts:
        # carefully
        try:
            # make each one
            attempt()
        # it must be refused
        except pyre.db.exceptions.NotSupportedError as error:
            # saying why
            assert "runs no statements" in str(error), str(error)
        # if it is not
        else:
            # say so
            assert False, "a folder ran a statement"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
