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
class HDF5(Library, family='pyre.externals.hdf5'):
    """
    The package manager for HDF5 packages
    """

    # constants
    category = 'hdf5'


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
            package=package, filenames=[host.dynamicLibrary(stem=cls.category)])
        # all done
        return


    # support for specific package managers
    @classmethod
    def generic(cls):
        """
        Provide a default implementation of HDF5
        """
        # there is only one...
        return Default


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Identify the default implementation of HDF5 on macports machines
        """
        # there is only one variation of this
        yield cls.generic()(name=cls.category)

        # and nothing else
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a HDF5 package instance on a macports host
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
class Default(LibraryInstallation, family='pyre.externals.hdf5.default', implements=HDF5):
    """
    A generic HDF5 installation
    """

    # constants
    version = 'unknown'
    category = HDF5.category


# end of file
