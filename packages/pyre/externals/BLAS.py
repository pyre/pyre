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


    # configuration verification
    @classmethod
    def checkConfiguration(cls, package):
        """
        Verify that the {package} is configured correctly
        """
        # get the host
        host = cls.pyre_host
        # check the location of the headers
        yield from cls.checkIncdir(
            package=package, filenames=["{}.h".format(cls.category)])
        # check the location of the libraries
        yield from cls.checkLibdir(
            package=package, filenames=[host.staticLibrary(stem=cls.category)])
        # all done
        return


    @classmethod
    def macportsChooseImplementations(cls, macports):
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


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a BLAS package instance on a macports host
        """
        # all the implementations currently supported leave headers and libraries in the
        # standard places, so there isn't much to do...

        # get the prefix
        prefix = macports.prefix()
        # apply the configuration
        instance.prefix = prefix
        instance.incdir = os.path.join(prefix, 'include')
        instance.libdir = os.path.join(prefix, 'lib')

        # all done
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

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"


# atlas
class Atlas(Default, family='pyre.externals.blas.atlas'):
    """
    Atlas BLAS support
    """

    # constants
    flavor = 'atlas'

    # framework hooks
    def pyre_configured(self):
        """
        Verify my configuration
        """
        # initialize my error list
        errors = []
        # get the host
        host = self.pyre_host

        # check the location of the headers
        errors += list(BLAS.checkIncdir(
            package=self, filenames=["cblas.h"]))
        # check the location of the libraries
        errors += list(BLAS.checkLibdir(
            package=self,
            filenames=[
                host.staticLibrary(stem='cblas'),
                host.staticLibrary(stem='atlas'),
            ]))
        # all done
        return errors


# OpenBLAS
class OpenBLAS(Default, family='pyre.externals.blas.openblas'):
    """
    OpenBLAS support
    """

    # constants
    flavor = 'openblas'

    # framework hooks
    def pyre_configured(self):
        """
        Verify my configuration
        """
        # initialize my error list
        errors = []
        # get the host
        host = self.pyre_host

        # check the location of the headers
        errors += list(BLAS.checkIncdir(
            package=self, filenames=["cblas_openblas.h"]))
        # check the location of the libraries
        errors += list(BLAS.checkLibdir(
            package=self,
            filenames=[
                host.dynamicLibrary(stem='openblas'),
            ]))
        # all done
        return errors


# gslcblas
class GSLCBLAS(Default, family='pyre.externals.blas.gsl'):
    """
    GSL BLAS support
    """

    # constants
    flavor = 'gsl'

    # framework hooks
    def pyre_configured(self):
        """
        Verify my configuration
        """
        # initialize my error list
        errors = []
        # get the host
        host = self.pyre_host

        # check the location of the headers
        errors += list(BLAS.checkIncdir(
            package=self, filenames=["gsl/gsl_cblas.h"]))
        # check the location of the libraries
        errors += list(BLAS.checkLibdir(
            package=self, filenames=[host.dynamicLibrary(stem='gslcblas')]))
        # all done
        return errors


# end of file
