# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


"""
This package provides access to the set of builtin constraints.

Constraints are predicates that raise a {ConstraintViolationError} exception whenever the value
they were asked to validate fails to meet their specific criteria. They are frequently used to
validate trait values supplied by the end-user.

The factories in this package build constraint instances out of the given input parameters that
specify a constraint. These instances can be later used to verify that values satisfy them by
calling the {validate} method of the constraint, or more simply, by using the constraint itself
as a function.

For example:

    import pyre.constraints
    g = pyre.constraints.isGreater(value=0)
    # check that the value 10 satisfies it
    g.validate(10)
    # or, equivalently
    g(10)

is one way you could implement the constraint "check that value is a positive number" and use
it to check that 10 does indeed statisfy it.

Instead of being functions that return booleans, constraints throw exceptions when they are
violated. This design choice is motivated by the observation that it is not always possible to
handle a constraint violation locally, since the caller may not have enough information to
handle the failure.
"""


def isAll(*constraints):
    """
    Passes when all the constraints in its list pass
    """
    # get the factory
    from .And import And
    # instantiate and return
    return And(*constraints)


def isAny(*constraints):
    """
    Passes when any of the constraints in its list passes
    """
    # get the factory
    from .Or import Or
    # instantiate and return
    return Or(*constraints)


def isBetween(*, low, high):
    """
    Check that a numeric value is between {low} and {high}
    """
    # get the factory
    from .Between import Between
    # instantiate and return
    return Between(low, high)


def isEqual(*, value):
    """
    Check that a numeric value is equal to {value}
    """
    # get the factory
    from .Equal import Equal
    # instantiate and return
    return Equal(value)


def isGreater(*, value):
    """
    Check that a numeric value is greater than {value}
    """
    # get the factory
    from .Greater import Greater
    # instantiate and return
    return Greater(value)


def isGreaterEqual(*, value):
    """
    Check that a numeric value is greater or equal to {value}
    """
    # get the factory
    from .GreaterEqual import GreaterEqual
    # instantiate and return
    return GreaterEqual(value)


def isLess(*, value):
    """
    Check that a numeric value is less than {value}
    """
    # get the factory
    from .Less import Less
    # instantiate and return
    return Less(value)


def isLessEqual(*, value):
    """
    Check that a numeric value is less than or equal to {value}
    """
    # get the factory
    from .LessEqual import LessEqual
    # instantiate and return
    return LessEqual(value)


def isLike(*, regexp):
    """
    Check that the value matches {regexp}, where {regexp} is a re-style regular expression. See
    the re builtin module
    """
    # get the factory
    from .Like import Like
    # instantiate and return
    return Like(regexp)


def isMember(*choices):
    """
    Check that the value supplied is one of {choices}
    """
    # get the factory
    from .Set import Set
    # instantiate and return
    return Set(*choices)


def isNot(constraint):
    """
    Check that value makes {constraint} fail
    """
    # get the factory
    from .Not import Not
    # instantiate and return
    return Not(constraint)


def isSubset(*, choices):
    """
    Check that the given set is a subset of {choices}
    """
    # get the factory
    from .Subset import Subset
    # instantiate and return
    return Subset(choices)


def isNegative():
    """
    Check that the given value is less than zero
    """
    # easy enough
    return isLess(value=0)


def isNonNegative():
    """
    Check that the given value is greater than or equal to zero
    """
    # easy enough
    return isGreaterEqual(value=0)


def isPositive():
    """
    Check that the given value is greater than zero
    """
    # easy enough
    return isGreater(value=0)


# end of file
