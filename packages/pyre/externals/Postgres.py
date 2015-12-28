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

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a postgres package instance on a macports host
        """
        # attempt to identify the package name from the {instance}
        package = macports.identifyPackage(package=instance)
        # get and save the package contents
        contents = tuple(macports.contents(package=package))
        # and the version info
        version, variants = macports.info(package=package)

        # look for 'psql'; all postgres implementations have one
        psql = 'psql'
        # to identify the {bindir}
        bindir = macports.findfirst(target=psql, contents=contents)

        # look for the main header file
        header = "libpq-fe.h"
        # find the folder
        incdir = macports.findfirst(target=header, contents=contents)

        # find my library
        libpq = cls.pyre_host.dynamicLibrary('pq')
        # find the folder
        libdir = macports.findfirst(target=libpq, contents=contents)

        # get the prefix
        prefix = os.path.commonpath([bindir, incdir, libdir])
        # apply the configuration
        instance.prefix = prefix
        instance.version = version
        instance.incdir = incdir
        instance.libdir = libdir
        instance.psql = os.path.join(bindir, psql)

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
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"

    psql = pyre.properties.str()
    psql.doc = "the location of my client"


# end of file
