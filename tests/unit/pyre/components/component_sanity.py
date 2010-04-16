#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: declare a trivial component
"""


def test():
    from pyre.components.Component import Component

    class component(Component, family="trivial"):
        """a trivial component"""

     
    return


# main
if __name__ == "__main__":
    test()


# end of file 
