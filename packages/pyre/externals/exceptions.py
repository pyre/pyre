# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# the framework wide base error
from ..framework.exceptions import FrameworkError


# the local base
class ExternalsError(FrameworkError):
    """
    Base class for all errors raised while discovering and resolving external packages
    """


# requirement parsing failures
class RequirementSyntaxError(ExternalsError):
    """
    Exception raised when a requirement specification cannot be parsed
    """

    # the error message template
    description = "could not parse the requirement '{0.spec}': {0.problem}"

    # meta-methods
    def __init__(self, spec, problem, **kwds):
        # chain up
        super().__init__(**kwds)
        # record the offending specification
        self.spec = spec
        # and what went wrong with it
        self.problem = problem
        # all done
        return


# end of file
