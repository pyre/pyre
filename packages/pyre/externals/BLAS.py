# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import pyre
# superclass
from .Library import Library


# the blas package manager
class BLAS(Library, family='pyre.externals.blas'):
    """
    The package manager for BLAS packages
    """

    # constants
    category = 'cblas'


    # support for specific package managers
    @classmethod
    def dpkgChoices(cls, dpkg):
        """
        Identify the default implementation of BLAS on dpkg machines
        """
        # complain
        raise NotImplementedError("NYI!")


    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of BLAS on macports machines
        """
        # on macports, the following packages provide support for BLAS, ranked by their
        # performance: atlas, openblas, gsl
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

    # public state
    libraries = pyre.properties.strings()
    libraries.doc = 'the libraries to place on the link line'


# atlas
class Atlas(Default, family='pyre.externals.blas.atlas'):
    """
    Atlas BLAS support
    """

    # constants
    flavor = 'atlas'

    # public state
    defines = pyre.properties.strings(default="WITH_ATLAS")
    defines.doc = "the compile time markers that indicate my presence"


    # configuration
    def macports(self, macports):
        """
        Attempt to repair my configuration
        """
        # the name of the macports package
        package = 'atlas'
        # attempt to
        try:
            # get the version info
            self.version, _ = macports.info(package=package)
        # if this fails
        except KeyError:
            # this package is not installed
            msg = 'the package {!r} is not installed'.format(package)
            # complain
            raise self.ConfigurationError(configurable=self, errors=[msg])
        # otherwise, grab the package contents
        contents = tuple(macports.contents(package=package))

        # in order to identify my {incdir}, search for the top-level header file
        header = 'cblas.h'
        # find it and extract the directory
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        libatlas = self.pyre_host.staticLibrary('atlas')
        # find it
        self.libdir = macports.findfirst(target=libatlas, contents=contents)
        # set my library list
        self.libraries = 'cblas', 'atlas'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# OpenBLAS
class OpenBLAS(Default, family='pyre.externals.blas.openblas'):
    """
    OpenBLAS support
    """

    # constants
    flavor = 'openblas'

    # public state
    defines = pyre.properties.strings(default="WITH_OPENBLAS")
    defines.doc = "the compile time markers that indicate my presence"


    # configuration
    def macports(self, macports):
        """
        Attempt to repair my configuration
        """
        # the name of the macports package
        package = 'OpenBLAS'
        # attempt to
        try:
            # get the version info
            self.version, _ = macports.info(package=package)
        # if this fails
        except KeyError:
            # this package is not installed
            msg = 'the package {!r} is not installed'.format(package)
            # complain
            raise self.ConfigurationError(configurable=self, errors=[msg])
        # otherwise, grab the package contents
        contents = tuple(macports.contents(package=package))

        # in order to identify my {incdir}, search for the top-level header file
        header = 'cblas_openblas.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        libopenblas = self.pyre_host.dynamicLibrary('openblas')
        # find it
        self.libdir = macports.findfirst(target=libopenblas, contents=contents)
        # set my library
        self.libraries = 'openblas'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# gslcblas
class GSLCBLAS(Default, family='pyre.externals.blas.gsl'):
    """
    GSL BLAS support
    """

    # constants
    flavor = 'gsl'

    # public state
    defines = pyre.properties.strings(default="WITH_GSLCBLAS")
    defines.doc = "the compile time markers that indicate my presence"


    # configuration
    def macports(self, macports):
        """
        Attempt to repair my configuration
        """
        # the name of the macports package
        package = 'gsl'
        # attempt to
        try:
            # get the version info
            self.version, _ = macports.info(package=package)
        # if this fails
        except KeyError:
            # this package is not installed
            msg = 'the package {!r} is not installed'.format(package)
            # complain
            raise self.ConfigurationError(configurable=self, errors=[msg])
        # otherwise, grab the package contents
        contents = tuple(macports.contents(package=package))

        # in order to identify my {incdir}, search for the top-level header file
        header = 'gsl/gsl_cblas.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        libgsl = self.pyre_host.dynamicLibrary('gslcblas')
        # find it
        self.libdir = macports.findfirst(target=libgsl, contents=contents)
        # set my library
        self.libraries = 'gslcblas'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# end of file
