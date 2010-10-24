#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Load records from a csv file
"""


def test():
    import pyre.tabular

    # build the target tuple
    target = [
        ("4000", "50", "tomatoes"),
        ("4001", "25", "pepers"),
        ("4002", "15", "grapes"),
        ("4003", "75", "kiwis"),
        ("4004", "50", "lemons"),
        ("4005", "50", "oranges"),
        ]

    # setup the csv data source
    columns = ["sku", "margin", "description"]
    source = pyre.tabular.record.csv_read(filename="vegetables.csv", columns=columns)

    # check
    for given, loaded in zip(target, source):
        assert given == loaded

    return


# main
if __name__ == "__main__":
    test()


# end of file 
