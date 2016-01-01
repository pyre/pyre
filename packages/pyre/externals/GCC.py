# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os, re, subprocess
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
        # get my category
        category = cls.category
        # on macports, gcc is a package group
        for package in macports.alternatives(group=category):
            # assume it's a good gcc installation and hand it to the caller
            yield Default(name=package)

        # and nothing else
        return


# superclass
from .ToolInstallation import ToolInstallation


# the implementation of a GCC installation
class Default(ToolInstallation, family='pyre.externals.gcc.default', implements=GCC):
    """
    A generic GCC installation
    """

    # constants
    category = GCC.category

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
        # chain up
        package, contents = super().macports(macports=macports)

        # compute the prefix
        self.prefix = macports.prefix()

        # form the target
        target = os.path.join(self.bindir[0], 'gcc-mp-.+')
        # find my wrapper
        for match in macports.find(target=target, pile=contents):
            # pull the body
            self.wrapper = match.group()

        # all done
        return package, contents


    # interface
    @pyre.export
    def binaries(self, packager, **kwds):
        """
        Generate a sequence of required executables
        """
        # try this
        yield 'gcc-mp-.+'
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
