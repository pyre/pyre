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


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
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

            # instantiate the package and return it
            yield factory(name=alternative)

        # out of ideas
        return


    # dpkg
    @classmethod
    def dpkgChoices(cls, dpkg):
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


# the base class
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
    launcher = pyre.properties.str()
    launcher.doc = 'the name of the launcher of MPI jobs'


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
        # chain up
        package, contents = super().macports(macports=macports)
        # compute the prefix
        self.prefix = os.path.commonpath(self.bindir + self.incdir + self.libdir)
        # find my launcher
        self.launcher, *_ = macports.locate(
            targets = self.binaries(packager=macports),
            paths = self.bindir)

        # all done
        return package, contents


    # interface
    @pyre.export
    def defines(self):
        """
        Generate a sequence of compile time macros that identify my presence
        """
        # the category marker
        yield "WITH_" + self.category.upper()
        # the flavor marker
        yield "WITH_" + self.flavor.upper()
        # all done
        return


    @pyre.export
    def headers(self, **kwds):
        """
        Generate a sequence of required header files
        """
        # only one
        yield 'mpi.h'
        # all done
        return


    @pyre.export
    def libraries(self, **kwds):
        """
        Generate a sequence of required libraries
        """
        # build my library name and hand it over
        yield self.category
        # all done
        return


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


    # protocol obligations
    @pyre.export
    def binaries(self, **kwds):
        """
        Generate a sequence of required executables
        """
        # look for the launcher
        yield 'mpirun-openmpi-gcc5'
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


    # protocol obligations
    @pyre.export
    def binaries(self, packager, **kwds):
        """
        Generate a sequence of required executables
        """
        if packager.name == 'macports':
            print('hola: {.pyre_name}'.format(self))

        # look for the launcher
        yield 'mpirun-mpich-gcc5'
        # all done
        return


# end of file
