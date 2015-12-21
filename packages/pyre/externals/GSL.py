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
class GSL(Library, family='pyre.externals.gsl'):
    """
    The package manager for GSL packages
    """

    # constants
    category = 'gsl'


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
            package=package, filenames=["{0}/{0}_version.h".format(cls.category)])
        # check the location of the libraries
        yield from cls.checkLibdir(
            package=package, filenames=[host.dynamicLibrary(stem=cls.category)])
        # all done
        return


    # support for specific package managers
    @classmethod
    def generic(cls):
        """
        Provide a default implementation of GSL
        """
        # there is only one...
        return Default


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Identify the default implementation of GSL on macports machines
        """
        # there is only one variation of this
        yield cls.generic()(name=cls.category)

        # and nothing else
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a GSL package instance on a macports host
        """
        # attempt to
        try:
            # get my package info
            version, variants = macports.info(package=cls.category)
        # if this fails
        except KeyError:
            # not much to do...
            return

        # get the prefix
        prefix = macports.prefix()
        # apply the configuration
        instance.prefix = prefix
        instance.version = version
        instance.incdir = os.path.join(prefix, 'include')
        instance.libdir = os.path.join(prefix, 'lib')

        # all done
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

    prefix = pyre.properties.str(default='/usr')
    prefix.doc = 'the package installation directory'

    incdir = pyre.properties.str(default='/usr/include')
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str(default='/usr/lib')
    libdir.doc = "the location of my libraries; for the linker command path"


# end of file
