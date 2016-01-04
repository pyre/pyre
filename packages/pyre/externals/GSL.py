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


# the gsl package manager
class GSL(Library, family='pyre.externals.gsl'):
    """
    The package manager for GSL packages
    """

    # constants
    category = 'gsl'


    # support for specific package managers
    @classmethod
    def dpkgChoices(cls, dpkg):
        """
        Identify the default implementation of GSL on dpkg machines
        """
        # complain
        raise NotImplementedError("NYI!")


    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of GSL on macports machines
        """
        # there is only one variation of this
        yield Default(name=cls.category)
        # and nothing else
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
    falvor = category

    # public state
    defines = pyre.properties.strings(default="WITH_GSL")
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
        header = 'gsl/gsl_version.h'
        # find it
        incdir = macports.findfirst(target=header, contents=contents)
        # and save it
        self.incdir = [incdir.parent] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        libgsl = self.pyre_host.dynamicLibrary('gsl')
        # find it
        libdir = macports.findfirst(target=libgsl, contents=contents)
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = 'gsl'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.incdir+self.libdir)

        # all done
        return


# end of file
