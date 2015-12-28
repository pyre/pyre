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
from .Tool import Tool
from .Library import Library


# the mpi package manager
class MPI(Tool, Library, family='pyre.externals.mpi'):
    """
    The package manager for MPI packages
    """

    # constants
    category = 'mpi'

    # user configurable state
    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'


    # configuration verification
    @classmethod
    def checkConfiguration(cls, package):
        """
        Verify that package ins configured correctly
        """
        # get the host
        host = cls.pyre_host
        # check the location of the binaries
        yield from cls.checkBindir(package=package, filenames=[package.launcher])
        # check the location of the headers
        yield from cls.checkIncdir(package=package, filenames=["mpi.h"])
        # check the location of the libraries
        yield from cls.checkLibdir(package=package, filenames=[host.dynamicLibrary(stem='mpi')])
        # all done
        return


    # support for specific package managers
    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of MPI on macports machines, starting with
        the package the user has selected as the default
        """
        # on macports, mpi is a package group
        for alternative in macports.alternatives(group=cls.category):
            # if the package name starts with 'openmpi'
            if alternative.startswith(OpenMPI.flavor):
                # use OpenMPI
                factory = OpenMPI
            # if it starts with 'mpich'
            elif alternative.startswith(MPICH.flavor):
                # use MPICH
                factory = MPICH
            # otherwise
            else:
                # this is a bug...
                import journal
                # so complain
                raise journal.firewall('pyre.externals.MPI').log(
                    "unknown MPI flavor for package {!r}".format(alternative))

            # attempt to
            try:
                # show me
                # instantiate the package and return it
                yield factory(name=alternative)
            # if this fails
            except factory.ConfigurationError:
                # try something else
                continue

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure an MPI package instance on a macports host
        """
        # get my category
        category = cls.category
        # attempt to identify the package name from the {instance}
        package = macports.identifyPackage(package=instance)
        # get and save the package contents
        contents = tuple(macports.contents(package=package))
        # and the version info
        version, variants = macports.info(package=package)

        # look for 'mpirun'; all MPI implementations have one
        launcher = 'mpirun-{}'.format(package)
        # to identify the {bindir}
        bindir = macports.findfirst(target=launcher, contents=contents)

        # look for the main header file
        header = 'mpi.h'
        # to identify the {incdir}
        incdir = macports.findfirst(target=header, contents=contents)

        # look for my library
        libmpi = cls.pyre_host.dynamicLibrary(category)
        # to identify the {libdir}
        libdir = macports.findfirst(target=libmpi, contents=contents)

        # compute the prefix
        prefix = os.path.commonpath([bindir, incdir, libdir])

        # apply the configuration
        instance.version = version
        instance.prefix = prefix
        instance.bindir = bindir
        instance.incdir = incdir
        instance.libdir = libdir
        instance.launcher = os.path.join(bindir, 'mpirun')

        # all done
        return


    # dpkg
    @classmethod
    def dpkgChooseImplementations(cls, dpkg):
        """
        Identify the default implementation of MPI on dpkg machines
        """
        # the list of the necessary openmpi packages
        openmpi = ["openmpi-bin", "libopenmpi-dev"]
        # check
        for package in openmpi:
            # attempt to
            try:
                # locate it
                dpkg.info(package)
            # if not there
            except KeyError:
                # look no further
                break
        # if they are all present
        else:
            # get openmpi and return it
            yield OpenMPI

        # the list of the necessary mpich packages
        mpich = ["mpich-bin", "libmpich-dev"]
        # check
        for package in mpich:
            # attempt to
            try:
                # locate it
                dpkg.info(package)
            # if not there
            except KeyError:
                # look no further
                break
        # if they are all present
        else:
            # get mpich and return it
            yield MPICH

        # out of ideas
        return


# superclass
from .ToolInstallation import ToolInstallation
from .LibraryInstallation import LibraryInstallation


# the openmpi package manager
class Default(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.mpi.default', implements=MPI):
    """
    The package manager for unknown MPI installations
    """

    # constants
    flavor = "unknown"
    category = MPI.category

    # public state
    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'


# the openmpi package manager
class OpenMPI(Default, family='pyre.externals.mpi.openmpi'):
    """
    The package manager for OpenMPI packages
    """

    # constants
    flavor = "openmpi"
    category = MPI.category


    # configuration strategies for specific package managers
    def dpkg(self, dpkg):
        """
        Attempt to repair the configuration of this instance assuming a dpkg host
        """
        # get the version
        self.version, _ = dpkg.info(package='libopenmpi-dev')

        # point directly to my own directories to bypass the links set up by {update-alternatives}
        prefix = '/usr/lib/openmpi'
        self.prefix = prefix
        self.bindir = os.path.join('/usr/bin')
        self.incdir = os.path.join(prefix, 'include')
        self.libdir = os.path.join(prefix, 'lib')
        self.launcher = os.path.join(self.bindir, 'mpirun.openmpi')

        # check my configuration again
        errors = self.pyre_configured()
        # and if there are errors
        if errors:
            # complain
            raise self.ConfigurationError(component=self, errors=errors)
        # all done
        return


# the mpich package manager
class MPICH(Default, family='pyre.externals.mpi.mpich'):
    """
    The package manager for MPICH packages
    """

    # constants
    flavor = "mpich"
    category = MPI.category

    # public state
    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'


    # configuration strategies for specific package managers
    def dpkg(self, dpkg):
        """
        Attempt to repair the configuration of this instance assuming a dpkg host
        """
        # get the version
        self.version, _ = dpkg.info(package='libmpich-dev')

        # point directly to my own directories to bypass the links set up by {update-alternatives}
        prefix = '/usr/lib/mpich'
        self.prefix = prefix
        self.bindir = os.path.join('/usr/bin')
        self.incdir = os.path.join(prefix, 'include')
        self.libdir = os.path.join(prefix, 'lib')
        self.launcher = os.path.join(self.bindir, 'mpirun.mpich')

        # check my configuration again
        errors = self.pyre_configured()
        # and if there are errors
        if errors:
            # complain
            raise self.ConfigurationError(component=self, errors=errors)
        # all done
        return


# end of file
