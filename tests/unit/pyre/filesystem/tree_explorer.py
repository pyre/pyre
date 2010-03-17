#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise the simple filesystem explorer
"""


def test():
    import pyre.filesystem

    fs = pyre.filesystem.newVirtualFilesystem()
    tools = fs.createFolder("/home/users/mga/dv/tools")
    tools.createFolder("bin").createNode("hello")
    tools.createFolder("lib").createNode("libhello.a")

    explorer = pyre.filesystem.newTreeExplorer()
    contents = explorer.explore(fs)

    assert contents == [
        " / (d)",
        " `- home (d)",
        "    `- users (d)",
        "       `- mga (d)",
        "          `- dv (d)",
        "             `- tools (d)",
        "                +- bin (d)",
        "                |  `- hello (f)",
        "                `- lib (d)",
        "                   `- libhello.a (f)",
        ]

    return


# main
if __name__ == "__main__":
    test()


# end of file 
