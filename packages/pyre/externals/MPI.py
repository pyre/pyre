# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os, pathlib
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
        # known installations
        known = [ OpenMPI, MPICH ]
        # on macports, mpi is a package group
        for alternative in macports.alternatives(group=cls.category):
            # go through the known installations
            for installation in known:
                # if the package name starts with the installation flavor
                if alternative.startswith(installation.flavor):
                    # instantiate the package and return it
                    yield installation(name=alternative)
                # otherwise
                else:
                    # this is a bug...
                    import journal
                    # so complain
                    raise journal.firewall('pyre.externals.MPI').log(
                        "unknown MPI flavor for package {!r}".format(alternative))

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
    libraries = pyre.properties.strings()
    libraries.doc = 'the libraries to place on the link line'

    launcher = pyre.properties.str()
    launcher.doc = 'the name of the launcher of MPI jobs'


    # configuration

    # these methods are invoked after construction if the instance is determined to be in
    # invalid state that was not the user's fault. typically this means that the package
    # configuration is still in its default state. the dispatcher determines the correct
    # package manager and forwards to one of the handlers in this section

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
        # ask macports for help; start by finding out which package supports me
        package = macports.identify(installation=self)
        # get the version info
        self.version, _ = macports.info(package=package)
        # and the package contents
        contents = tuple(macports.contents(package=package))

        # {mpi} is a selection group
        group = self.category
        # the package deposits its selection alternative here
        selection = str(macports.prefix() / 'etc' / 'select' / group / '(?P<alternate>.*)')
        # so find it
        match = next(macports.find(target=selection, pile=contents))
        # extract the name of the alternative
        alternative = match.group('alternate')
        # ask for the normalization data
        normalization = macports.getNormalization(group=group, alternative=alternative)
        # build the normalization map
        nmap = { base: target for base,target in zip(*normalization) }
        # find the binary that supports {mpirun} and use it to set my launcher
        self.launcher = nmap[pathlib.Path('bin/mpirun')].name
        # extract my {bindir}
        bindir = macports.findfirst(target=self.launcher, contents=contents)
        # and save it
        self.bindir = [ bindir ] if bindir else []

        # in order to identify my {incdir}, search for the top-level header file
        header = 'mpi.h'
        # find it
        incdir = macports.findfirst(target=header, contents=contents)
        # and save it
        self.incdir = [incdir.parent] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        libmpi = self.pyre_host.dynamicLibrary('mpi')
        # find it
        libdir = macports.findfirst(target=libmpi, contents=contents)
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = 'mpi_cxx', 'mpi'

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.bindir+self.incdir+self.libdir)

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

    # public state
    defines = pyre.properties.strings(default="WITH_OPENMPI")
    defines.doc = "the compile time markers that indicate my presence"


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
    defines = pyre.properties.strings(default="WITH_MPICH")
    defines.doc = "the compile time markers that indicate my presence"


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

        # all done
        return


# end of file
