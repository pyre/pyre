# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the framework
import pyre

# my protocol
from .PackageManager import PackageManager


# declaration
class Bare(pyre.component, family="pyre.packagers.bare", implements=PackageManager):
    """
    Support for un*x systems that don't have package management facilities
    """

    # constants
    name = "bare"

    # protocol obligations
    @pyre.export
    def prefix(self):
        """
        The package manager install location
        """
        # don't have one
        return ""

    @pyre.export
    def installed(self):
        """
        Retrieve available information for all installed packages
        """
        # don't have any
        return ()

    @pyre.export
    def packages(self, category):
        """
        Generate a sequence of package names with compatible installations for the given
        package {category}.
        """
        # don't have any
        return ()

    @pyre.export
    def info(self, package):
        """
        Return information about the given {package}
        """
        # don't know anything
        raise KeyError(package)

    @pyre.export
    def contents(self, package):
        """
        Generate a sequence of the contents of the {package}
        """
        # don't know anything
        raise KeyError(package)

    @pyre.export
    def configure(self, installation):
        """
        Dispatch to the {packageInstance} configuration procedure that is specific to a host
        without a specific package manager
        """
        # what she said...
        return installation.bare(manager=self)


# end of file
