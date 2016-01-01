# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os, sys
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
        # this is a macports host; ask it for all the cython package choices
        for alternative in macports.alternatives(group=cls.category):
            # convert the selection alias into the package name that provides it
            package = macports.getSelectionInfo(group=cls.category, alternative=alternative)
            # instantiate each one using the package name and hand it to the caller
            yield Default(name=package)

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
        # chain up
        package, contents = super().macports(macports=macports)

        # compute the prefix
        self.prefix, _ = os.path.split(self.bindir[0])
        # find my compiler
        self.compiler, *_ = macports.locate(
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
        # the compiler
        yield self.category
        # all done
        return


# end of file
