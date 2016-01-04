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


# the cython package manager
class Cython(Tool, family='pyre.externals.cython'):
    """
    The package manager for the cython interpreter
    """

    # constants
    category = 'cython'

    # user configurable state
    compiler = pyre.properties.str()
    compiler.doc = 'the name of the compiler; may be the full path to the executable'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Provide alternative compatible implementations of cython on macports machines, starting
        with the package the user has selected as the default
        """
        # on macports, {cython3} and {cython2} are in the same package group; try cython3.x
        # installations followed by cython 2.x
        versions = [ Cython3, Cython2 ]
        # go through my choices
        for version in versions:
            # ask macports for all available alternatives
            for package in macports.alternatives(group=version.category):
                # instantiate each one using the package name and hand it to the caller
                yield version(name=package)

        # out of ideas
        return


# superclass
from .ToolInstallation import ToolInstallation


# the cython package manager
class Default(
        ToolInstallation,
        family='pyre.externals.cython.default', implements=Cython):
    """
    The package manager for cython instances
    """

    # constants
    category = Cython.category
    flavor = category

    # public state
    compiler = pyre.properties.str()
    compiler.doc = 'the name of the cython compiler'


    # configuration
    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # NYI
        raise NotImplementedError('NYI!')


    def macports(self, macports):
        """
        Attempt to repair my configuration
        """
        # ask macports for help; start by finding out which package is related to me
        package = macports.identify(installation=self)
        # get the version info
        self.version, _ = macports.info(package=package)
        # and the package contents
        contents = tuple(macports.contents(package=package))

        # {cython} is a selection group
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
        # find the binary that supports {cython} and use it to set my compiler
        self.compiler = nmap[pathlib.Path('bin/cython')].name
        # look for it to get my {bindir}
        bindir = macports.findfirst(target=self.compiler, contents=contents)
        # and save it
        self.bindir = [ bindir ] if bindir else []

        # now that we have everything, compute the prefix
        self.prefix = self.bindir[0].parent

        # all done
        return


# cython 2
class Cython2(Default, family='pyre.externals.cython.cython2'):
    """
    The package manager for cython 2.x instances
    """

    # constants
    flavor = Default.flavor + '2'


# cython 3
class Cython3(Default, family='pyre.externals.cython.cython3'):
    """
    The package manager for cython 3.x instances
    """

    # constants
    flavor = Default.flavor + '3'


# end of file
