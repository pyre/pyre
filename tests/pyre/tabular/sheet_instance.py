#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Build a rudimentary table
"""


import pyre.tabular


class pricing(pyre.tabular.sheet):
    """
    The sheet layout
    """

    sku = pyre.tabular.auto()
    production = pyre.tabular.auto()
    shipping = pyre.tabular.auto()
    margin = pyre.tabular.auto()
    overhead = pyre.tabular.auto()


def test():
    # make a sheet
    p = pricing(name="vegetables")
    # and return it
    return p


# main
if __name__ == "__main__":
    test()


# end of file 
