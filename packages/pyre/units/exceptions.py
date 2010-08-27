# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


# exceptions
from ..framework.exceptions import FrameworkError


class UnitError(FrameworkError):
    """
    Base class for all errors generated by this package
    """

    def __init__(self, operand, **kwds):
        super().__init__(**kwds)
        self.operand = operand
        return


class InvalidConversion(UnitError):
    """
    Exception raised when an attempt was made to convert a dimensional quantity to a
    float. This typically happens when a math package function is invoked with a dimensional
    argument
    """

    def __init__(self, operand, **kwds):
        super().__init__(
            operand=operand, description="cannot convert unit instance to float", **kwds)
        return


class IncompatibleUnits(UnitError):
    """
    Exception raised when the operands of a binary operator have imcompatible units such as
    adding lengths to times
    """

    def __init__(self, operand, **kwds):
        super().__init__(
            operand=operand,
            description="cannot {!r} quantites with incompatible units".format(operand))
        return


# end of file 
