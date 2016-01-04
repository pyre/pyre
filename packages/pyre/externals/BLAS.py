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
    def dpkgAlternatives(cls, dpkg):
        """
        Go through the installed packages and identify those that are relevant for providing
        support for my installations
        """
        # get the index of installed packages
        installed = dpkg.installed()

        # the ATLAS development packages
        atlas = 'libatlas-base-dev', 'libatlas-dev'
        # find the missing ones
        missing = [ pkg for pkg in atlas if pkg not in installed ]
        # if there are no missing ones
        if not missing:
            # hand back a pyre safe name and the list of packages
            yield Atlas.flavor, atlas

        # the OpenBLAS development packages
        openblas = 'libopenblas-dev', 'libopebblas-base'
        # find the missing ones
        missing = [ pkg for pkg in atlas if pkg not in installed ]
        # if there are no missing ones
        if not missing:
            # hand back a pyre safe name and the list of packages
            yield OpenBLAS.flavor, openblas

        # the GSL development packages
        gsl = 'libgsl0-dev',
        # find the missing ones
        missing = [ pkg for pkg in atlas if pkg not in installed ]
        # if there are no missing ones
        if not missing:
            # hand back a pyre safe name and the list of packages
            yield GSLCBLAS.flavor, gsl

        # all done
        return


    @classmethod
    def dpkgChoices(cls, dpkg):
        """
        Identify the default implementation of BLAS on dpkg machines
        """
        # ask {dpkg} for my options
        alternatives = sorted(dpkg.alternatives(group=cls), reverse=True)
        # the order of preference of these implementations
        versions = Atlas, OpenBLAS, GSLCBLAS
        # go through each one
        for version in versions:
           # scan through the alternatives
            for name in alternatives:
                # if it is match
                if name.startswith(version.flavor):
                    # build an instance and return it
                    yield version(name=name)

        # out of ideas
        return


    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of BLAS on macports machines
        """
        # on macports, the following packages provide support for BLAS, ranked by their
        # performance: atlas, openblas, gsl
        versions = Atlas, OpenBLAS, GSLCBLAS
        # get the index of installed packages
        installed = macports.getInstalledPackages()
        # go through each one
        for version in versions:
            # get the flavor
            flavor = version.flavor
            # look for an installation
            if flavor in installed:
                # build an instance and return it
                yield version(name=flavor)

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
    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # get the names of the packages that support me
        lib, headers = dpkg.identify(installation=self)
        # get the version info
        self.version, _ = dpkg.info(package=lib)

        # in order to identify my {incdir}, search for the top-level header file
        header = 'atlas/atlas_buildinfo.h'
        # find the header
        incdir = dpkg.findfirst(target=header, contents=dpkg.contents(package=headers))
        # which is inside the atlas directory; save the parent
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        stem = self.flavor
        # convert it into the actual file name
        libatlas = self.pyre_host.dynamicLibrary(stem)
        # find it
        libdir = dpkg.findfirst(target=libatlas, contents=dpkg.contents(package=lib))
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)
        # all done
        return


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
        header = 'atlas/atlas_buildinfo.h'
        # look for it
        incdir = macports.findfirst(target=header, contents=contents)
        # it is inside the atlas directory; save the parent
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        libatlas = self.pyre_host.staticLibrary('atlas')
        # look for
        libdir = macports.findfirst(target=libatlas, contents=contents)
        # and save it
        self.libdir = [ libdir ] if libdir else []
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
    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # get the names of the packages that support me
        dev, *_ = dpkg.identify(installation=self)
        # get the version info
        self.version, _ = dpkg.info(package=dev)

        # in order to identify my {incdir}, search for the top-level header file
        header = 'openblas/openblas_config.h'
        # find the header
        incdir = dpkg.findfirst(target=header, contents=dpkg.contents(package=dev))
        # which is inside the atlas directory; save the parent
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        stem = self.flavor
        # convert it into the actual file name
        libatlas = self.pyre_host.dynamicLibrary(stem)
        # find it
        libdir = dpkg.findfirst(target=libatlas, contents=dpkg.contents(package=dev))
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)
        # all done
        return


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
        incdir = macports.findfirst(target=header, contents=contents)
        # and save it
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        libopenblas = self.pyre_host.dynamicLibrary('openblas')
        # find it
        libdir = macports.findfirst(target=libopenblas, contents=contents)
        # and save it
        self.libdir = [ libdir ] if libdir else []
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
    flavor = 'gslcblas'

    # public state
    defines = pyre.properties.strings(default="WITH_GSLCBLAS")
    defines.doc = "the compile time markers that indicate my presence"


    # configuration
    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # get the names of the packages that support me
        dev, *_ = dpkg.identify(installation=self)
        # get the version info
        self.version, _ = dpkg.info(package=dev)

        # in order to identify my {incdir}, search for the top-level header file
        header = 'gsl/gsl_cblas.h'
        # find the header
        incdir = dpkg.findfirst(target=header, contents=dpkg.contents(package=dev))
        # which is inside the atlas directory; save the parent
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        stem = self.flavor
        # convert it into the actual file name
        libgsl = self.pyre_host.dynamicLibrary(stem)
        # find it
        libdir = dpkg.findfirst(target=libgsl, contents=dpkg.contents(package=dev))
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


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
        incdir = macports.findfirst(target=header, contents=contents)
        # and save it
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        stem = self.flavor
        # convert it into the actual file name
        libgsl = self.pyre_host.dynamicLibrary('gslcblas')
        # find it
        libdir = macports.findfirst(target=libgsl, contents=contents)
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = 'gslcblas'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# end of file
