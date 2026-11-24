#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server writes an array as postgres writes it: its levels in braces, its
entries separated by commas, null as NULL, and the entries that would be misread in double quotes
"""


def test():
    """
    Load arrays of integers and of text into a folder, and check the lines of its file
    """
    # externals
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
        # and some labels
        labels = pyre.db.array(schema=pyre.db.str())

    # the folder, named after this driver and kept for inspection
    folder = "folder_array_text"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_array_text", path=folder).attach()
    # make the table
    db.createTable(Sample)
    # load a sample with values that need care
    db.load(
        Sample.pyre_immutable(
            id=1,
            cells=((1, 2), (3, None)),
            labels=("plain", "a b", "c,d", 'say "hi"', "back\\slash", "", "NULL", "{x}", None),
        ),
        # and one with empty arrays
        Sample.pyre_immutable(id=2, cells=(), labels=()),
    )
    # read the file
    with open(f"{folder}/samples.tsv") as stream:
        # all of it
        text = stream.read()
    # the lines it must hold; the backslashes inside the arrays are doubled again by the copy
    expected = (
        "1\t{{1,2},{3,NULL}}\t"
        '{plain,"a b","c,d","say \\\\"hi\\\\"","back\\\\\\\\slash","","NULL","{x}",NULL}\n'
        "2\t{}\t{}\n"
    )
    # check
    assert text == expected, text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
