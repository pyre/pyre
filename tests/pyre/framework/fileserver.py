#!/usr/bin/env python
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
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the fileserver
    fs = executive.fileserver
    assert fs is not None

    # get hold of the system node
    system = fs["/system"]
    assert system is not None

    # get hold of the user node
    user = fs["/user"]
    assert user is not None

    # dump the filesystem
    fs.dump(False) # switch to True to see the dump

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
