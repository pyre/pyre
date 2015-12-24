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
                host.dynamicLibrary('{0.category}CommonCore-{0.eigenversion}'.format(package))
            ])
        # all done
        return


    # support for specific package managers
    @classmethod
    def generic(cls):
        """
        Provide a default implementation of VTK
        """
        # there is only one...
        return Default


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Identify the default implementation of VTK on macports machines
        """
        # there is only one variation of this
        yield cls.generic()(name=cls.category)

        # and nothing else
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a VTK package instance on a macports host
        """
        # get the instance name
        name = instance.pyre_name
        # attempt to
        try:
            # interpret the name as an installed package
            version, variants = macports.info(package=name)
        # if this fails
        except KeyError:
            # not much to do...
            return

        # this is an installed package; get its contents
        contents = macports.contents(package=name)

        # look for
        header = "(?P<incdir>.*)/vtkVersion.h"
        # to identify the include path
        incdir = macports.incdir(regex=header, contents=contents)

        # find my library
        libvtk = "(?P<libdir>.*)/{}".format(cls.pyre_host.dynamicLibrary('vtkCommonCore.*'))
        # find the folder
        libdir = macports.libdir(regex=libvtk, contents=contents)

        # get the prefix
        prefix = macports.prefix()
        # apply the configuration
        instance.prefix = prefix
        instance.version = version
        instance.incdir = incdir
        instance.libdir = libdir

        # on macports, the version numbers of the installed libraries do not match the package
        # version, so we build a truncate version number (major, minor) to use while verifying
        # the configuration

        # attempt to
        try:
            # split the version
            major, minor, *_ = version.split('.')
        # if it can't be done
        except ValueError:
            # no worries
            instance.eigenversion = version
        # otherwise
        else:
            # assemble
            instance.eigenversion = "{}.{}".format(major, minor)

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
    eigenversion = 'unknown'

    # public state
    prefix = pyre.properties.str(default='/usr')
    prefix.doc = 'the package installation directory'

    incdir = pyre.properties.str(default='/usr/include')
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str(default='/usr/lib')
    libdir.doc = "the location of my libraries; for the linker command path"


# end of file
