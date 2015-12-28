# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, re, subprocess
# access to the framework
import pyre
# superclass
from .Tool import Tool


# the mpi package manager
class GCC(Tool, family='pyre.externals.gcc'):
    """
    The package manager for GCC installations
    """

    # constants
    category = 'gcc'

    # public state
    wrapper = pyre.properties.str(default='gcc')
    wrapper.doc = "the name of the compiler front end"


    # configuration verification
    @classmethod
    def checkConfiguration(cls, package):
        """
        Verify that the {package} is configured correctly
        """
        # check the location of the binaries
        yield from cls.checkBindir(package=package, filenames=[package.wrapper])
        # all done
        return


    # support for specific package managers
    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Identify the default implementation of GCC on macports machines
        """
        # get my category
        category = cls.category
        # on macports, gcc is a package group
        for package in macports.alternatives(group=category):
            # assume it's a good GCC installation and hand it to the caller
            yield Suite(name=package)

        # and nothing else
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a GCC package instance on a macports host
        """

        # get my category
        category = cls.category
        # attempt to identify the package name from the {instance}
        package = macports.identifyPackage(package=instance)
        # get and save the package contents
        contents = tuple(macports.contents(package=package))
        # and the version info
        version, variants = macports.info(package=package)

        # get the macports prefix
        prefix = macports.prefix()
        # the {bindir} is always known
        bindir = os.path.join(prefix, 'bin')

        # my wrapper starts with
        pattern = os.path.join(bindir, 'gcc-mp-')
        # go through the contents of the package
        for item in contents:
            # if this item matches my patter
            if item.startswith(pattern):
                # save it
                wrapper = item
                # and bail
                break
        # otherwise
        else:
            # i know nothing; this will cause a configuration failure elsewhere
            warpper = None

        # apply the configuration
        instance.prefix = prefix
        instance.version = version
        instance.bindir = bindir
        instance.wrapper = wrapper

        # all done
        return


# superclass
from .ToolInstallation import ToolInstallation


# the implementation of a GCC installation
class Suite(ToolInstallation, family='pyre.externals.gcc.default', implements=GCC):
    """
    A generic GCC installation
    """

    # constants
    version = 'unknown'
    category = GCC.category

    # public state
    wrapper = pyre.properties.str()
    wrapper.doc = "the name of the compiler front end"

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
    prefix = pyre.properties.str(default='/usr')
    prefix.doc = 'the package installation directory'

    bindir = pyre.properties.str(default='/usr/bin')
    bindir.doc = "the location of my binaries"

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
