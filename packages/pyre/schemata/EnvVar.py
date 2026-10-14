# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# superclass
from .String import String


# declaration
class EnvVar(String):
    """
    A type declarator for strings whose default values are associated with an environment variable
    """

    # constants
    typename = "envvar"  # the name of my type

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an environment variable
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onEnvVar
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, variable, **kwds):
        # compute the default value by attempting to read the value from the environment
        default = os.environ.get(variable, str())
        # chain up
        super().__init__(default=default, **kwds)
        # save the variable name
        self.envvar = variable
        # all done
        return


# end of file
