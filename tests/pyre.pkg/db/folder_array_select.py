#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server reads back the arrays it writes, level by level, each entry in the
type of the entries of its column
"""


def test():
    """
    Load arrays of several types into a folder, select them, and compare
    """
    # externals
    import datetime
    import shutil

    # access the package
    import pyre.db

    # a table of samples
    class Sample(pyre.db.table, id="samples"):
        """
        Samples
        """

        # the key
        id = pyre.db.int().primary()
        # the cells of a grid
        cells = pyre.db.array(schema=pyre.db.int(), rank=2)
        # some labels
        labels = pyre.db.array(schema=pyre.db.str())
        # some moments
        moments = pyre.db.array(schema=pyre.db.timestamp())
        # some flags
        flags = pyre.db.array(schema=pyre.db.bool())
        # and some octets
        blobs = pyre.db.array(schema=pyre.db.bytes())

    # the values of the samples, by column
    samples = [
        (
            1,
            ((1, 2), (3, None)),
            (
                "plain",
                "a b",
                "c,d",
                'say "hi"',
                "back\\slash",
                "",
                "NULL",
                "{x}",
                "tab\there",
                None,
            ),
            (datetime.datetime(2026, 11, 24, 1, 2, 3), None),
            (True, False, None),
            (b"\x00\xff", b""),
        ),
        (2, (), (), (), (), ()),
        (3, None, None, None, None, None),
    ]
    # the names of the columns
    names = [field.name for field in Sample.pyre_fields]

    # the folder, named after this driver and kept for inspection
    folder = "folder_array_select"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_array_select", path=folder).attach()
    # make the table
    db.createTable(Sample)
    # load the samples
    db.load(*(Sample.pyre_immutable(**dict(zip(names, values))) for values in samples))
    # read them back
    selected = [tuple(row) for row in db.select(query=Sample)]
    # they are the ones that went in, in order
    assert selected == samples, selected
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
