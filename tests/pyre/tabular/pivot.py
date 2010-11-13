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


class cost(pyre.tabular.sheet):
    """The prices of things"""
    # layout
    sku = pyre.tabular.str()
    sku.index = True

    description = pyre.tabular.str()
    production = pyre.tabular.float()
    overhead = pyre.tabular.float()
    shipping = pyre.tabular.float()
    margin = pyre.tabular.float()


class sales(pyre.tabular.sheet):
    """The transaction data"""
    # layout
    date = pyre.tabular.str()
    time = pyre.tabular.str()
    sku = pyre.tabular.str()
    quantity = pyre.tabular.float()
    discount = pyre.tabular.float()
    sale = pyre.tabular.float()


def test():
    # make a csv reader
    csv = pyre.tabular.csv()
    # make a sheet
    vegetables = cost(name="vegetables")
    transactions = sales(name="sales")
    # populate the tables
    csv.read(sheet=transactions, uri="sales.csv")
    csv.read(sheet=vegetables, uri="vegetables.csv")
    # and return the sheets
    return vegetables, sales


# main
if __name__ == "__main__":
    test()


# end of file 
