# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# externals
import os, sys
# access to the framework
import pyre
# superclass
from .Tool import Tool
from .Library import Library


# the python package manager
class Python(Tool, Library, family='pyre.externals.python'):
    """
    The package manager for the python interpreter
    """

    # constants
    category = 'python'

    # user configurable state
    interpreter = pyre.properties.str()
    interpreter.doc = 'the full path to the interpreter'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Provide alternative compatible implementations of python on macports machines, starting
        with the package the user has selected as the default
        """
        # on macports, {python3} and {python2} are separate package groups; try python3.x
        # installations followed by python 2.x
        versions = [ Python3, Python2 ]
        # go through my choices
        for version in versions:
            # ask macports for all available alternatives
            for package in macports.alternatives(group=version.flavor):
                # instantiate each one using the package name and hand it to the caller
                yield version(name=package)

        # out of ideas
        return


# implementation superclasses
from .ToolInstallation import ToolInstallation
from .LibraryInstallation import LibraryInstallation


# the base class for python installations
class Default(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.python.default', implements=Python):
    """
    The base class for for python instances
    """

    # constants
    flavor = Python.category
    category = Python.category

    # public state
    interpreter = pyre.properties.str()
    interpreter.doc = 'the full path to the python interpreter'


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
        self.prefix = os.path.commonpath(self.bindir + self.incdir + self.libdir)
        # find my interpreter
        self.interpreter, *_ = macports.locate(
            targets = self.binaries(packager=macports),
            paths = self.bindir)

        # all done
        return package, contents


    # interface
    @pyre.export
    def binaries(self, **kwds):
        """
        Generate a sequence of required executables
        """
        # only one, typically named after my flavor
        yield self.flavor
        # all done
        return


    @pyre.export
    def defines(self):
        """
        Generate a sequence of compile time macros that identify my presence
        """
        # the python marker
        yield "WITH_" + self.flavor.upper()
        # all done
        return


    @pyre.export
    def headers(self, **kwds):
        """
        Generate a sequence of required header files
        """
        # only one
        yield 'Python.h'
        # all done
        return


    @pyre.export
    def libraries(self, **kwds):
        """
        Generate a sequence of required libraries
        """
        # get the host
        host = self.pyre_host
        # build my library name and hand it over
        yield self.category + self.sigver()
        # all done
        return


    # implementation details
    def sigver(self):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # get my version
        version = self.version
        # attempt to
        try:
            # split my version into major, minor and the rest
            major, minor, *rest = version.split('.')
        # if i don't have enough fields
        except ValueError:
            # can't do much
            return version
        # otherwise, assemble the significant part and return it
        return '{}.{}'.format(major, minor)


# the python 2.x package manager
class Python2(Default, family='pyre.externals.python.python2'):
    """
    The package manager for python 2.x instances
    """

    # constants
    flavor = Default.flavor + '2'


# the python 3.x package manager
class Python3(Default, family='pyre.externals.python.python3'):
    """
    The package manager for python 3.x instances
    """

    # constants
    flavor = Default.flavor + '3'


# end of file
