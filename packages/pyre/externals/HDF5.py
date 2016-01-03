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


# the hdf5 package manager
class HDF5(Library, family='pyre.externals.hdf5'):
    """
    The package manager for HDF5 packages
    """

    # constants
    category = 'hdf5'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of HDF5 on macports machines
        """
        # there is only one variation of this
        yield Default(name=cls.category)
        # and nothing else
        return


# superclass
from .LibraryInstallation import LibraryInstallation


# the implementation
class Default(LibraryInstallation, family='pyre.externals.hdf5.default', implements=HDF5):
    """
    A generic HDF5 installation
    """

    # constants
    category = HDF5.category
    flavor = category

    # public state
    defines = pyre.properties.strings(default="WITH_HDF5")
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
        package = 'hdf5'
        # attempt to
        try:
            # get the version info
            self.version, _ = macports.info(package=package)
        # if this fails
        except KeyError:
            # this package is not installed
            msg = 'the package {!r} is not installed'.format(package)
            # clear any previous configuration errors; they are now irrelevant
            self.pyre_configurationErrors = []
            # complain
            raise self.ConfigurationError(configurable=self, errors=[msg])
        # otherwise, grab the package contents
        contents = tuple(macports.contents(package=package))

        # in order to identify my {incdir}, search for the top-level header file
        header = 'hdf5.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        libhdf5 = self.pyre_host.dynamicLibrary('hdf5')
        # find it
        self.libdir = macports.findfirst(target=libhdf5, contents=contents)
        # set my library
        self.libraries = 'hdf5'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# end of file
