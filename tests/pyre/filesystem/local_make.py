#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Create and dump a local filesystem
"""

# externals
import os


def test(interactive=False): # change to True to see the dump
    # access the package
    import pyre.filesystem
    # make a local filesystem
    home = pyre.filesystem.local(root=".")
    home.discover()
    home.dump(interactive) # change to True to see the dump

    # create a template
    tmp = pyre.filesystem.virtual()
    tmp['sample/one'] = tmp.folder()
    tmp['sample/two'] = tmp.folder()

    # realize it
    home.make(name="local-make", tree=tmp)
    home.discover()
    home.dump(interactive) # change to True to see the dump

    # check that what we expect is there
    cwd = os.getcwd()
    path = 'local-make/sample/one'
    assert home[path].uri == os.path.join(cwd,path)
    path = 'local-make/sample/two'
    assert home[path].uri == os.path.join(cwd,path)

    return home


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.filesystem" }
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()

    # check that the nodes were all destroyed
    from pyre.filesystem.Node import Node
    # print("Node extent:", len(Node._pyre_extent))
    assert len(Node._pyre_extent) == 0


# end of file
