#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Execrices the nameserver
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the nameserver
    ns = executive.nameserver
    assert ns is not None

    # get hold of the system node
    system = ns["/system"]
    assert system is not None

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
