# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
# access to the framework
import pyre
# superclass
from .Tool import Tool
from .Library import Library


# the postgres package manager
class Postgres(Tool, Library, family='pyre.externals.postgres'):
    """
    The package manager for postgres client development
    """

    # constants
    category = 'pq'

    # user configurable state
    psql = pyre.properties.str()
    psql.doc = 'the full path to the postgres client'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of postgres on macports machines
        """
        # on macports, postgres is a package group
        for package in macports.alternatives(group='postgresql'):
            # if the package name starts with 'postgresql'
            if package.startswith('postgresql'):
                # use the default implementation
                yield Default(name=package)

        # out of ideas
        return


# superclasses
from .ToolInstallation import ToolInstallation
from .LibraryInstallation import LibraryInstallation


# the implementation
class Default(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.postgres.default', implements=Postgres):
    """
    A generic postgres installation
    """

    # constants
    category = Postgres.category

    # user configurable state
    psql = pyre.properties.str()
    psql.doc = 'the full path to the postgres client'


    # configuration
    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # NYI
        raise NotImplementedError('NYI!')


    def macports(self, macports, **kwds):
        """
        Attempt to repair my configuration
        """
        # chain up
        package, contents = super().macports(macports=macports, **kwds)
        # compute the prefix
        self.prefix = macports.prefix()
        # find my client
        self.psql, *_ = macports.locate(
            targets = self.binaries(packager=macports),
            paths = self.bindir)
        # all done
        return package, contents


    # protocol obligations
    @pyre.export
    def binaries(self, **kwds):
        """
        Generate a sequence of required executables
        """
        # the name of the client executable
        yield 'psql'
        # all done
        return


    @pyre.export
    def defines(self):
        """
        Generate a sequence of compile time macros that identify my presence
        """
        # just one
        yield "WITH_" + self.category.upper()
        # all done
        return


    # interface
    @pyre.export
    def headers(self, **kwds):
        """
        Generate a sequence of required header files
        """
        # my main header
        yield 'libpq-fe.h'
        # all done
        return


    @pyre.export
    def libraries(self, **kwds):
        """
        Generate a sequence of required libraries
        """
        # my implementations
        yield 'pq'
        # all done
        return


# end of file
