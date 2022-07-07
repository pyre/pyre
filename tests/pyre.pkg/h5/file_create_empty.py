#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


"""
Create an empty file
"""


# the driver
def test():
    # support
    import pyre

    # fix the location of the test file
    path = pyre.primitives.path("file_create_empty.h5")
    # create it
    f = pyre.h5.file().open(path=path, mode="w")

    # verify it's there
    assert path.exists()
    # and delete it
    path.unlink()

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
