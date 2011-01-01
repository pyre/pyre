#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that improperly formed input source raise predicatble exceptions
"""


def test():
    
    import pyre.records
    csv = pyre.records.csv()

    # try to read without providing a valid data source
    try:
        tuple(csv.read(layout=pyre.records.record))
        assert False
    except csv.SourceSpecificationError as error:
        assert error.description == "invalid input source specification"

    return csv


# main
if __name__ == "__main__":
    test()


# end of file 
