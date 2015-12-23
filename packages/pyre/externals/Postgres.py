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
class Postgres(Library, family='pyre.externals.postgres'):
    """
    The package manager for postgres client development
    """

    # constants
    category = 'pq'


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
            package=package, filenames=["lib{}-fe.h".format(cls.category)])
        # check the location of the libraries
        yield from cls.checkLibdir(
            package=package, filenames=[host.dynamicLibrary(stem=cls.category)])
        # all done
        return


    # support for specific package managers
    @classmethod
    def generic(cls):
        """
        Provide a default implementation of postgres
        """
        # there is only one...
        return Default


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Identify the default implementation of postgres on macports machines
        """
        # on macports, postgres is a package group
        for package in macports.alternatives(group='postgresql'):
            # if the package name starts with 'postgresql'
            if package.startswith('postgresql'):
                # use the default implementation
                yield Default(name=package)

        # if we get this far, try this
        yield cls.generic()(name=cls.category)

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a postgres package instance on a macports host
        """
        # get my name
        name = instance.pyre_name
        # attempt to
        try:
            # get my package info
            version, variants = macports.info(package=name)
        # if this fails
        except KeyError:
            # not much to do...
            return

        # get my selection info
        packageName, contents, smap = macports.getSelectionInfo(
            group='postgresql', alternative=name)

        # the header regex
        header = "(?P<incdir>.*)/libpq-fe.h$"
        # find the folder
        incdir = macports.incdir(regex=header, contents=contents)

        # find my library
        libmpi = "(?P<libdir>.*)/{}".format(cls.pyre_host.dynamicLibrary('pq'))
        # find the folder
        libdir = macports.libdir(regex=libmpi, contents=contents)

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
class Default(
        LibraryInstallation,
        family='pyre.externals.postgres.default', implements=Postgres):
    """
    A generic postgres installation
    """

    # constants
    category = Postgres.category

    # public state
    prefix = pyre.properties.str(default='/usr')
    prefix.doc = 'the package installation directory'

    incdir = pyre.properties.str(default='/usr/include')
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str(default='/usr/lib')
    libdir.doc = "the location of my libraries; for the linker command path"



# end of file
