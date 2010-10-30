#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Load partial records from a csv file
"""


def test():
    import pyre.records

    # layout the record
    class item(pyre.records.record):
        # the fields
        sku = pyre.records.field()
        margin = pyre.records.field()
        description = pyre.records.field()
        # type information
        sku.type = pyre.schema.str
        margin.type = pyre.schema.float
        description.type = pyre.schema.str

    # build the target tuple
    target = [
        ("4000", 50, "tomatoes"),
        ("4001", 25, "pepers"),
        ("4002", 15, "grapes"),
        ("4003", 75, "kiwis"),
        ("4004", 50, "lemons"),
        ("4005", 50, "oranges"),
        ]

    # create the reader
    csv = pyre.records.csv()
    # read the csv data 
    source = csv.read(layout=item, uri="vegetables.csv")
    # check
    for given, loaded in zip(target, source):
        assert given == loaded

    return


# main
if __name__ == "__main__":
    test()


# end of file 
