# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework
import pyre


# declaration
class PackageManager(pyre.protocol, family="pyre.platforms.packagers"):
    """
    The obligations of package database engines

    Engines encapsulate a source of information about installed software: a real package
    manager such as macports or dpkg, a conda environment, or plain filesystem probing of
    well known locations. They interpret package {recipes}, i.e. declarative descriptions of
    what a package category looks like on disk, and convert them into configured trait values
    for package installations
    """

    # requirements
    @pyre.provides
    def about(self):
        """
        A phrase identifying this database, for provenance records
        """

    @pyre.provides
    def prefix(self):
        """
        The root of the package database installations
        """

    @pyre.provides
    def available(self):
        """
        Check whether this engine is functional on this host
        """

    @pyre.provides
    def installed(self):
        """
        Retrieve available information for all installed packages
        """

    @pyre.provides
    def info(self, package):
        """
        Return the available information about {package}

        This method should succeed if and only if {package} is actually fully installed
        """

    @pyre.provides
    def contents(self, package):
        """
        Generate a sequence of the files installed by {package}
        """

    @pyre.provides
    def resolve(self, recipe):
        """
        Map {recipe} onto the name of an installed package that provides it, if any
        """

    @pyre.provides
    def configure(self, recipe):
        """
        Interpret {recipe} against my package database and return a map of installation trait
        values, or {None} if the package is not installed here
        """

    # framework obligations
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Build the preferred engine implementation
        """
        # the host should specify a sensible default; if there is nothing there, this is an
        # unmanaged system that relies on filesystem probing of standard locations
        from .Bare import Bare

        # return the support for unmanaged systems
        return Bare


# end of file
