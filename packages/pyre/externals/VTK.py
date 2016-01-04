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


# the vtk package manager
class VTK(Library, family='pyre.externals.vtk'):
    """
    The package manager for VTK packages
    """

    # constants
    category = 'vtk'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of VTK on macports machines
        """
        # version 6.x installations
        yield VTK6(name=cls.category)
        # version 5.x installations
        yield VTK5(name=cls.category+'5')
        # and nothing else
        return


# superclass
from .LibraryInstallation import LibraryInstallation


# the implementation
class VTK5(LibraryInstallation, family='pyre.externals.vtk.vtk5', implements=VTK):
    """
    Support for VTK 5.x installations
    """

    # constants
    category = VTK.category
    flavor = category + '5'

    # public state
    defines = pyre.properties.strings(default="WITH_VTK6")
    defines.doc = "the compile time markers that indicate my presence"

    libraries = pyre.properties.strings()
    libraries.doc = 'the libraries to place on the link line'


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
        # the name of the macports package
        package = 'vtk5'
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
        # grab the package contents
        contents = tuple(macports.contents(package=package))

        # in order to identify my {incdir}, search for the top-level header file
        header = 'vtkVersion.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        stem = 'vtkCommonCore'
        # convert it into a library
        libvtk = self.pyre_host.dynamicLibrary(stem)
        # find it
        self.libdir = macports.findfirst(target=libvtk, contents=contents)
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# the implementation
class VTK6(LibraryInstallation, family='pyre.externals.vtk.vtk6', implements=VTK):
    """
    Support for VTK 6.x installations
    """

    # constants
    category = VTK.category
    flavor = category + '6'

    # public state
    defines = pyre.properties.strings(default="WITH_VTK6")
    defines.doc = "the compile time markers that indicate my presence"

    libraries = pyre.properties.strings()
    libraries.doc = 'the libraries to place on the link line'


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
        # the name of the macports package
        package = 'vtk'
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
        self.version, _ = macports.info(package=package)
        # and the package contents
        contents = tuple(macports.contents(package=package))

        # in order to identify my {incdir}, search for the top-level header file
        header = 'vtkVersion.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        stem = self.libgen('CommonCore')
        # convert it into a library
        libvtk = self.pyre_host.dynamicLibrary(stem)
        # find it
        self.libdir = macports.findfirst(target=libvtk, contents=contents)
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


    # interface
    def libgen(self, stem):
        """
        Construct the name of a library given a capability {stem}
        """
        # build and return
        return 'vtk{}-{.sigver}'.format(stem, self)


# end of file
