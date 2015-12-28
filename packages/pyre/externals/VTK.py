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
class VTK(Library, family='pyre.externals.vtk'):
    """
    The package manager for VTK packages
    """

    # constants
    category = 'vtk'


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
            package=package, filenames=["vtkVersion.h".format(cls.category)])
        # check the location of the libraries
        yield from cls.checkLibdir(
            package=package,
            filenames=[
                host.dynamicLibrary('{0.category}CommonCore-*'.format(package))
            ])
        # all done
        return


    # support for specific package managers
    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Identify the default implementation of VTK on macports machines
        """
        # there is only one variation of this
        yield Default(name=cls.category)
        # and nothing else
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a VTK package instance on a macports host
        """
        # attempt to identify the package name from the {instance}
        package = macports.identifyPackage(package=instance)
        # get and save the package contents
        contents = tuple(macports.contents(package=package))
        # and the version info
        version, variants = macports.info(package=package)

        # look for
        header = "vtkVersion.h"
        # to identify the include path
        incdir = macports.findfirst(target=header, contents=contents)

        # find my library
        libvtk = cls.pyre_host.dynamicLibrary('vtkCommonCore.*')
        # find the folder
        libdir = macports.findfirst(target=libvtk, contents=contents)

        # get the prefix
        prefix = macports.prefix()
        # apply the configuration
        instance.prefix = prefix
        instance.version = version
        instance.incdir = incdir
        instance.libdir = libdir

        # all done
        return


# superclass
from .LibraryInstallation import LibraryInstallation
# the implementation
class Default(LibraryInstallation, family='pyre.externals.vtk.default', implements=VTK):
    """
    A generic VTK installation
    """

    # constants
    category = VTK.category

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"

    # interface
    def sigver(self, version=None):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # if the user didn't specify
        if version is None:
            # use mine
            version = self.version
        # split it into major, minor and the rest
        major, minor, *rest = version.split('.')
        # assemble the significant part
        return '{}.{}'.format(major, minor)


# end of file
