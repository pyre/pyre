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


# the mpi package manager
class BLAS(Library, family='pyre.externals.blas'):
    """
    The package manager for BLAS packages
    """

    # constants
    category = 'cblas'


    # support ofr specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of BLAS on macports machines
        """
        # on macports, the following possible packages provide support for BLAS, ranked by
        # their performance: atlas, openblas, gsl
        versions = [ Atlas, OpenBLAS, GSLCBLAS ]
        # get the index of installed packages
        installed = macports.getInstalledPackages()

        # go through each one
        for version in versions:
            # look for an installation
            if version.flavor in installed:
                # build an instance and return it
                yield version(name=version.flavor)

        # out of ideas
        return



# superclass
from .LibraryInstallation import LibraryInstallation


# the base class
class Default(LibraryInstallation, family='pyre.externals.blas.default', implements=BLAS):
    """
    A generic BLAS installation
    """

    # constants
    flavor = 'unknown'
    category = BLAS.category


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
        self.prefix = os.path.commonpath(self.incdir + self.libdir)
        # all done
        return package, contents


    # interface
    def defines(self):
        """
        Generate a sequence of compile time macros that identify my presence
        """
        # just one
        yield "WITH_" + self.flavor.upper()
        # all done
        return


# atlas
class Atlas(Default, family='pyre.externals.blas.atlas'):
    """
    Atlas BLAS support
    """

    # constants
    flavor = 'atlas'


    # configuration
    def macports(self, macports):
        """
        Attempt to repair my configuration
        """
        # chain up
        package, contents = super().macports(macports=macports, dynamic=False)
        # all done
        return package, contents


    # interface
    def headers(self):
        """
        Generate a sequence of required header files
        """
        # my main header
        yield 'cblas.h'
        # all done
        return


    def libraries(self):
        """
        Generate a sequence of required libraries
        """
        # the blas interface
        yield 'cblas'
        # my implementation
        yield 'atlas'
        # all done
        return


# OpenBLAS
class OpenBLAS(Default, family='pyre.externals.blas.openblas'):
    """
    OpenBLAS support
    """

    # constants
    flavor = 'OpenBLAS'


    # interface
    def headers(self):
        """
        Generate a sequence of required header files
        """
        # my main header
        yield 'cblas_openblas.h'
        # all done
        return


    def libraries(self):
        """
        Generate a sequence of required libraries
        """
        # my implementations
        yield 'openblas'
        # all done
        return


# gslcblas
class GSLCBLAS(Default, family='pyre.externals.blas.gsl'):
    """
    GSL BLAS support
    """

    # constants
    flavor = 'gsl'

    # interface
    def headers(self):
        """
        Generate a sequence of required header files
        """
        # my main header
        yield 'gsl/gsl_cblas.h'
        # all done
        return


    def libraries(self):
        """
        Generate a sequence of required libraries
        """
        # my implementations
        yield 'gslcblas'
        # all done
        return


# end of file
