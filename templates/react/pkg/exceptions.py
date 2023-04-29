# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# get the framework
import pyre

# the base class for my exceptions
class {project.capname}Error(pyre.PyreError):
    """
    Base class for all {project.name} errors
    """

# component configuration errors
class ConfigurationError({project.capname}Error):
    """
    Exception raised when {project.name} components detect inconsistencies in their configurations
    """

    # public data
    description = "configuration error: {{0.reason}}"

    # meta-methods
    def __init__(self, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.reason = reason
        # all done
        return


# end of file
