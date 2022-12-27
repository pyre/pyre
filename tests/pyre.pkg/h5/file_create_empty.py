#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Create an empty file
"""


# the driver
def test():
    # support
    import pyre

    # fix the location of the test file
    uri = pyre.primitives.path("file_create_empty.h5")
    # create it
    f = pyre.h5.file().open(uri=uri, mode="w")

    # verify it's there
    assert uri.exists()
    # and delete it
    uri.unlink()

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
