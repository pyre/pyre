#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that folders can be instantiated and that their limited interface works as advertised
"""


def test():
    import pyre.filesystem

    # fake a filesystem
    class filesystem: pass
    # build a fake filesystem
    fs = filesystem()

    # build a folder
    folder = pyre.filesystem.folder(filesystem=fs)
    # and some nodes
    usr = folder.node()
    tmp = folder.node()
    home = folder.node()
    # add them to the folder
    folder.contents["usr"] = usr
    folder.contents["tmp"] = tmp
    folder.contents["home"] = home

    # count the children
    assert len(folder.contents) == 3

    # access the individual nodes
    assert usr == folder.contents["usr"]
    assert tmp == folder.contents["tmp"]
    assert home == folder.contents["home"]

    # all done
    return folder


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
