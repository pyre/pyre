#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table whose rows refer to other rows of the same table is reproduced into a folder
"""


def test():
    """
    Reproduce three granules, the first derived from the last, from sqlite into a folder
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
        # and the granule it was derived from, if any
        source = pyre.db.str()

    # the granules refer to the granules they were derived from
    Granule.pyre_foreignKey(field=Granule.source, foreign=Granule.name)

    # the source, a database in memory
    source = pyre.db.sqlite(name="folder_reproduce_self_source").attach()
    # with the table
    source.createTable(Granule)
    # and three granules, the first derived from the last
    source.insert(
        Granule.pyre_immutable(name="a", source="c"),
        Granule.pyre_immutable(name="b", source=None),
        Granule.pyre_immutable(name="c", source="b"),
    )

    # the folder, named after this driver and kept for inspection
    folder = "folder_reproduce_self"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # the target
    target = pyre.db.folder(name="folder_reproduce_self", path=folder).attach()
    # reproduces the table
    target.reproduce(source=source, tables=(Granule,))
    # read the granules back
    derived = {row.name: row.source for row in target.select(query=Granule)}
    # they are all there, with their sources
    assert derived == {"a": "c", "b": None, "c": "b"}, derived
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
