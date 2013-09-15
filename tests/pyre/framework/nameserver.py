#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Exercises the fileserver
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the name server
    ns = executive.nameserver
    assert ns is not None

    # dump the namespace
    # ns.dump()

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
