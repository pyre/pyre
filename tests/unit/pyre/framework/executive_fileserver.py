#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Execrices the fileserver
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the fileserver
    ns = executive.fileserver
    assert ns is not None

    # get hold of the system node
    system = ns["/pyre/system"]
    assert system is not None

    # get hold of the user node
    user = ns["/pyre/user"]
    assert user is not None

    # dump the filesystem
    ns._dump(True) # switch to True to see the dump

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
