#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Build a rudimentary record
"""


import pyre.records


class interval(pyre.records.record):
    """
    A sample record
    """
    # field declarations
    left = pyre.records.field()
    right = pyre.records.field()

    # type information
    left.type = pyre.schema.float()
    right.type = pyre.schema.float()

    # constraints
    left.validators = pyre.constraints.isLess(value=0),
    right.validators = pyre.constraints.isGreater(value=0),


def test():
    # try to build a record
    try:
        interval(left=1, right=2)
        assert False
    except interval.ConstraintViolationError as error:
        assert error.constraint == interval.left.validators[0]
        assert error.value == 1
        
    # and again
    try:
        interval(left=-2, right=-1)
        assert False
    except interval.ConstraintViolationError as error:
        assert error.constraint == interval.right.validators[0]
        assert error.value == -1
        
    return interval


# main
if __name__ == "__main__":
    test()


# end of file 
