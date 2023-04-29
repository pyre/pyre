# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import os

# superclass
from .List import List


# declaration
class EnvPath(List):
    """
    A list of paths whose default value is tied to the value of an environment variable
    """

    # constants
    typename = "envpath"  # the name of my type
    pathsep = os.pathsep  # the character to use as separator

    # meta-methods
    def __init__(self, variable, pathsep=pathsep, **kwds):
        # save the path separator
        self.pathsep = pathsep
        # attempt to
        try:
            # get the value of the environment variable
            default = os.environ[variable]
        # if the variable is not defined
        except KeyError:
            # the default is an empty list
            default = []
        # otherwise
        else:
            # split it using the path separator
            default = list(filter(None, default.split(self.pathsep)))

        # chain up with {path} as my schema
        super().__init__(schema=self.path(), default=default, **kwds)

        # save the variable name
        self.envvar = variable
        # all done
        return

    # implementation details
    def _coerce(self, value, **kwds):
        """
        Convert {value} into an iterable
        """
        # all we have to do is split strings using the path separator
        if isinstance(value, str):
            # do the split
            value = value.split(self.pathsep)
        # everything else is handled by my superclass
        return super()._coerce(value=value, **kwds)


# end of file
