#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Create and dump a local filesystem
"""


def test():
    import pyre.filesystem

    # build a filesystem out of the current directory
    dot = pyre.filesystem.newLocalFilesystem(root=".").discover()
    # locate this file
    this = dot["local_open.py"]
    # turn it in to a stream and read its contents
    contents = this.open().readlines()
    # check the first line
    assert contents[0] == "#!/usr/bin/env python\n"
    # check the last line
    assert contents[-1] == "# end of file\n"

    return dot, this


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
