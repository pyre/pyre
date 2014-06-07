#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Exercises the fileserver
"""


def test():
    import pyre
    # access the fileserver
    fs = pyre.executive.fileserver
    # make sure we got one
    assert fs is not None

    # initialize it
    fs.initializeNamespace()

    # get hold of the package node
    packages = fs["/pyre/packages"]
    assert packages is not None

    # get hold of the user node
    user = fs["/pyre/user"]
    assert user is not None

    # dump the filesystem
    fs.dump(False) # switch to True to see the dump

    # all done
    return fs


# main
if __name__ == "__main__":
    test()


# end of file 
