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
from .Library import Library


# the hdf5 package manager
class HDF5(Library, family='pyre.externals.hdf5'):
    """
    The package manager for HDF5 packages
    """

    # constants
    category = 'hdf5'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of HDF5 on macports machines
        """
        # there is only one variation of this
        yield Default(name=cls.category)
        # and nothing else
        return


# superclass
from .LibraryInstallation import LibraryInstallation
# the implementation
class Default(LibraryInstallation, family='pyre.externals.hdf5.default', implements=HDF5):
    """
    A generic HDF5 installation
    """

    # constants
    category = HDF5.category


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
        yield 'hdf5.h'
        # all done
        return


    @pyre.export
    def libraries(self, **kwds):
        """
        Generate a sequence of required libraries
        """
        # my implementations
        yield 'hdf5'
        # all done
        return


# end of file
