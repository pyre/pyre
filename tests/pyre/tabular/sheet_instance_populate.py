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

    sku = pyre.tabular.measure()
    description = pyre.tabular.measure()
    production = pyre.tabular.measure()
    overhead = pyre.tabular.measure()
    shipping = pyre.tabular.measure()
    margin = pyre.tabular.measure()


def test():
    # make a sheet
    p = pricing(name="vegetables")

    # populate it
    p.populate(records=None)
    
    return p


# main
if __name__ == "__main__":
    test()


# end of file 
