# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os
# access to the framework
import pyre
# superclass
from .Library import Library


# the gsl package manager
class GSL(Library, family='pyre.externals.gsl'):
    """
    The package manager for GSL packages
    """

    # constants
    category = 'gsl'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of GSL on macports machines
        """
        # there is only one variation of this
        yield Default(name=cls.category)
        # and nothing else
        return


# superclass
from .LibraryInstallation import LibraryInstallation
# the implementation
class Default(LibraryInstallation, family='pyre.externals.gsl.default', implements=GSL):
    """
    A generic GSL installation
    """

    # constants
    category = GSL.category


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
        package, contents = super().macports(macports=macports, package=self.category, **kwds)
        # compute the prefix
        self.prefix = macports.prefix()
        # all done
        return package, contents


    # interface
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
        yield 'gsl/gsl_version.h'
        # all done
        return


    @pyre.export
    def libraries(self, **kwds):
        """
        Generate a sequence of required libraries
        """
        # my implementations
        yield 'gsl'
        # all done
        return


# end of file
