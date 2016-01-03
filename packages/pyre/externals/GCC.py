# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os, re, pathlib, subprocess
# access to the framework
import pyre
# superclass
from .Tool import Tool


# the gcc package manager
class GCC(Tool, family='pyre.externals.gcc'):
    """
    The package manager for GCC installations
    """

    # constants
    category = 'gcc'

    # public state
    wrapper = pyre.properties.str(default='gcc')
    wrapper.doc = "the name of the compiler front end"


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of GCC on macports machines
        """
        # the list of supported versions
        versions = [ GCC5 ]
        # go through my choices
        for version in versions:
            # ask macports for all available alternatives
            for package in macports.alternatives(group=version.flavor):
                # instantiate each one using the package name and hand it to the caller
                yield version(name=package)

        # out of ideas
        return


# superclass
from .ToolInstallation import ToolInstallation


# the implementation of a GCC installation
class GCC5(ToolInstallation, family='pyre.externals.gcc.gcc5', implements=GCC):
    """
    Support for GCC 5.x installations
    """

    # constants
    category = GCC.category
    flavor = category + '5'

    # public state
    wrapper = pyre.properties.str()
    wrapper.doc = "the name of the compiler front end"


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
        # ask macports for help; start by finding out which package supports me
        package = macports.identify(installation=self)
        # get the version info
        self.version, _ = macports.info(package=package)
        # and the package contents
        contents = tuple(macports.contents(package=package))

        # {gcc} is a selection group
        group = self.category
        # the package deposits its selection alternative here
        selection = str(macports.prefix() / 'etc' / 'select' / group / '(?P<alternate>.*)')
        # so find it
        match = next(macports.find(target=selection, pile=contents))
        # extract the name of the alternative
        alternative = match.group('alternate')
        # ask for the normalization data
        normalization = macports.getNormalization(group=group, alternative=alternative)
        # build the map
        nmap = { base: target for base,target in zip(*normalization) }
        # find the binary that supports {gcc} and use it to set my wrapper
        self.wrapper = nmap[pathlib.Path('bin/gcc')].name
        # set my {bindir}
        self.bindir = macports.findfirst(target=self.wrapper, contents=contents)

        # now that we have everything, compute the prefix
        self.prefix = self.bindir[0].parent

        # all done
        return


    # implementation details
    def retrieveVersion(self):
        """
        Get my version number directly from the compiler

        In general, this is not needed except on hosts with no package managers to help me
        """
        # set up the shell command
        settings = {
            'executable': self.wrapper,
            'args': (self.wrapper, '--version'),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout

            # the first line is the version
            line = next(stream).strip()
            # extract the fields
            match = self._versionRegex.match(line)
            # if it didn't match
            if not match:
                # oh well...
                return 'unknown'
            # otherwise, extract the clang version number
            return match.group('version')

        # all done
        return 'unknown'


    # private data
    _versionRegex = re.compile(r"gcc\s+\([^)]+\)\s+(?P<version>[.0-9]+)")


# Apple's clang
class CLang(ToolInstallation, family='pyre.externals.gcc.clang', implements=GCC):
    """
    Apple's clang
    """

    # constants
    category = GCC.category


    # public state
    wrapper = pyre.properties.str(default='/usr/bin/gcc')
    wrapper.doc = "the name of the compiler front end"


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # get the version
        self.version = self.retrieveVersion()
        # all done
        return


    # implementation details
    def retrieveVersion(self):
        """
        Get my version number
        """
        # set up the shell command
        settings = {
            'executable': self.wrapper,
            'args': (self.wrapper, '--version'),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout

            # the first line is the version
            line = next(stream).strip()
            # extract the fields
            match = self._versionRegex.match(line)
            # if it didn't match
            if not match:
                # oh well...
                return 'unknown'
            # otherwise, extract the clang version number
            return match.group('version')

        # all done
        return


    # private data
    _versionRegex = re.compile(r"Apple LLVM version [.0-9]+\s\(clang-(?P<version>[.0-9]+)\)$")


# end of file
