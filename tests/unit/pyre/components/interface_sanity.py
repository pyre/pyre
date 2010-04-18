#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: declare a trivial interface
"""


def test():
    # make one
    from pyre.components.Interface import Interface
    class interface(Interface):
        """a trivial interface"""
    # and return it
    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
