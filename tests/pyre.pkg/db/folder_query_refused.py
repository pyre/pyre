#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server reads only whole tables: a query, or a bound on the rows, is refused
"""


def test():
    """
    Ask a folder server for a query of a table, and for a table with a bound
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

    # the names of the granules
    class Names(pyre.db.query, granule=Granule):
        """
        The names of the granules
        """

        # the name
        name = granule.name

    # the folder, named after this driver and kept for inspection
    folder = "folder_query_refused"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_query_refused", path=folder).attach()
    # make the table
    db.createTable(Granule)
    # the attempts
    attempts = (
        # a query
        lambda: list(db.select(query=Names)),
        # and a table with a bound on its rows
        lambda: list(db.select(query=Granule, limit=1)),
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
            assert "whole tables" in str(error), str(error)
        # if it is not
        else:
            # say so
            assert False, "a folder read something other than a whole table"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
