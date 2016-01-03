# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os, pathlib
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
    category = 'postgresql'

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
    flavor = category

    # user configurable state
    psql = pyre.properties.str()
    psql.doc = 'the full path to the postgres client'

    defines = pyre.properties.strings(default="WITH_PQ")
    defines.doc = "the compile time markers that indicate my presence"

    libraries = pyre.properties.strings()
    libraries.doc = 'the libraries to place on the link line'


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
        # ask macports for help; start by finding out which package supports me
        package = macports.identify(installation=self)
        # get the version info
        self.version, _ = macports.info(package=package)
        # and the package contents
        contents = tuple(macports.contents(package=package))

        # {postgresql} is a selection group
        group = self.category
        # the package deposits its selection alternative here
        selection = str(macports.prefix() / 'etc' / 'select' / group / '(?P<alternate>.*)')
        # so find it
        match = next(macports.find(target=selection, pile=contents))
        # extract the name of the alternative
        alternative = match.group('alternate')
        # ask for the normalization data
        normalization = macports.getNormalization(group=group, alternative=alternative)
        # build the normalization map
        nmap = { base: target for base,target in zip(*normalization) }
        # find the binary that supports {psql} and use it to set my launcher
        self.psql = nmap[pathlib.Path('bin/psql')].name
        # set my {bindir}
        self.bindir = macports.findfirst(target=self.psql, contents=contents)

        # in order to identify my {incdir}, search for the top-level header file
        header = 'libpq-fe.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        libpq = self.pyre_host.dynamicLibrary('pq')
        # find it
        self.libdir = macports.findfirst(target=libpq, contents=contents)
        # set my library
        self.libraries = 'pq'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.bindir+self.incdir+self.libdir)

        # all done
        return


# end of file
