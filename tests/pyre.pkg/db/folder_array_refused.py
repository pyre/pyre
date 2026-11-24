#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server refuses the values of an array column, which it has no text for, and
names the column
"""


def test():
    """
    Load a row with an array into a folder
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
        # and the values
        values = pyre.db.array(schema=pyre.db.int())

    # the folder, named after this driver and kept for inspection
    folder = "folder_array_refused"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_array_refused", path=folder).attach()
    # make the table
    db.createTable(Sample)
    # carefully
    try:
        # load a sample
        db.load(Sample.pyre_immutable(id=1, values=(1, 2, 3)))
    # it must be refused
    except pyre.db.exceptions.NotSupportedError as error:
        # naming the column
        assert "samples.values" in str(error), str(error)
    # if it is not
    else:
        # say so
        assert False, "a folder wrote an array"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
