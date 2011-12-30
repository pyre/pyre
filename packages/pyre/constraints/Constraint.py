# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import abc


class Constraint(metaclass=abc.ABCMeta):
    """
    The base class for constraints
    """


    # interface
    @abc.abstractmethod
    def validate(self, candidate):
        """
        The default behavior for constraints is to raise a ConstraintViolationError.

        Override to implement a specific test
        """
        raise self.ConstraintViolationError(self, candidate)


    # function interface
    def __call__(self, candidate):
        """
        Interface to make constraints callable
        """
        return self.validate(candidate)


    # logical operations
    def __and__(self, other):
        """
        Enable the chaining of constraints using the logical operators
        """
        from .And import And
        return And(self, other)


    def __or__(self, other):
        """
        Enable the chaining of constraints using the logical operators
        """
        from .Or import Or
        return Or(self, other)


    # exceptions
    from .exceptions import ConstraintViolationError


# end of file 
