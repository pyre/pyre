# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# the framework
import pyre

# my superclass
from .Managed import Managed


# declaration
class Conda(Managed, family='pyre.platforms.packagers.conda'):
    """
    Support for conda environments
    """

    # public data
    @property
    def name(self):
        return "conda"

    @property
    def client(self):
        return "conda"

    # protocol obligations
    @pyre.export
    def prefix(self):
        """
        The conda environment prefix
        """
        # check the cache
        prefix = self._prefix
        # if we have done this before
        if prefix is not None:
            # return the cached value
            return prefix
        # get the environment variable
        conda_prefix = os.getenv("CONDA_PREFIX")
        # if not in a conda environment
        if not conda_prefix:
            # complain
            raise self.ConfigurationError(
                configurable=self, errors=["not in a conda environment: CONDA_PREFIX not set"]
            )
        # pathify and cache
        self._prefix = pyre.primitives.path(conda_prefix)
        # all done
        return self._prefix

    @pyre.export
    def installed(self):
        """
        Retrieve available information for all installed packages
        """
        # not needed for basic functionality
        return {}

    @pyre.export
    def info(self, package):
        """
        Return the available information about {package}
        """
        # not needed for basic functionality
        return {}

    @pyre.export
    def contents(self, package):
        """
        Retrieve the contents of a conda package
        """
        # not needed for basic functionality
        return []


# end of file
