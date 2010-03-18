#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that attempts to create local filesystems with nonexistent roots fails as expected
"""


def test():
    import pyre.filesystem

    home = pyre.filesystem.newLocalFilesystem(root="../../../..")
    home._dump(interactive=False) # change to True to see the dump

    return


# main
if __name__ == "__main__":
    test()


# end of file 
