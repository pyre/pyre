#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():

    from pyre.units.exceptions import (
        UnitError, InvalidConversion, IncompatibleUnits
        )

    try:
        raise UnitError(description=None, operand=None)
    except UnitError as error:
        pass

    try:
        raise InvalidConversion(operand=None)
    except InvalidConversion as error:
        pass

    try:
        raise IncompatibleUnits(operand=None)
    except IncompatibleUnits as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
