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
        Verify that package ins configured correctly
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
    def generic(cls, host):
        """
        Provide a default implementation of GSL
        """
        # there is only one...
        return GSLSTD


    @classmethod
    def macports(cls, host):
        """
        Identify the default implementation of GSL on macports machines
        """
        # there is only one variation of this
        return cls.generic(host=host)(name=cls.category)


    @classmethod
    def macportsConfigureInstance(cls, package, host):
        """
        Configure an GSL package instance on a macports host
        """
        # attempt to
        try:
            # get my package info
            version, variants = host.installed(package=cls.category)
        # if this fails
        except KeyError:
            # not much to do...
            return

        # get the prefix
        prefix = host.prefix()
        # set the prefix
        package.prefix = prefix
        # set incdir
        package.incdir = os.path.join(prefix, 'include')
        # set libdir
        package.libdir = os.path.join(prefix, 'lib')
        # set the version
        package.version = version

        # all done
        return


# superclass
from .LibraryInstallation import LibraryInstallation
# the implementation
class GSLSTD(LibraryInstallation, family='pyre.externals.gslstd', implements=GSL):
    """
    A generic GSL installation
    """

    # constants
    version = 'unknown'
    category = GSL.category


# end of file
