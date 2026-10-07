#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify creation of filesystems based on zipfiles
"""


def test():
    import os
    import zipfile
    import pyre.filesystem

    # the name of the zipfile, next to this driver, where it stays for inspection
    archive = "zip_open.zip"
    # the contents of this directory, taken before the archive appears in it, and without
    # the archive a previous run left behind
    names = [name for name in os.listdir(".") if name != archive]
    # build the archive
    target = zipfile.ZipFile(file=archive, mode="w")
    for filename in names:
        target.write(filename)
    target.close()

    # open it as a filesystem
    home = pyre.filesystem.zip(root=archive).discover()
    # locate this file
    this = home["zip_open.py"]
    # turn it into a stream and read its content
    contents = this.open().readlines()
    # check the first line
    assert contents[0] == b"#!/usr/bin/env python3\n"
    # check the last line
    assert contents[-1] == b"# end of file\n"

    return home


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    import pyre.filesystem

    test()


# end of file
