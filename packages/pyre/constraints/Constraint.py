# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# base class that sets the interface
class Constraint:
    """
    The base class for constraints
    """


    # exceptions
    from .exceptions import ConstraintViolationError


    # interface
    def validate(self, value, **kwds):
        """
        The default behavior for constraints is to raise a {ConstraintViolationError}.

        Override to implement a specific test
        """
        # complain
        raise self.ConstraintViolationError(self, value)


    # function interface
    def __call__(self, value, **kwds):
        """
        Interface to make constraints callable
        """
        # forward to my method
        return self.validate(value=value, **kwds)


    # logical operations
    def __and__(self, other):
        """
        Enable the chaining of constraints using logical {and}
        """
        # get the operator
        from .And import And
        # build a constraint and return it
        return And(self, other)


    def __or__(self, other):
        """
        Enable the chaining of constraints using logical {or}
        """
        # get the operator
        from .Or import Or
        # build a constraint and return it
        return Or(self, other)


# end of file
