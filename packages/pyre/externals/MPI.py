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
    def generic(cls):
        """
        Provide a default implementation of MPI on platforms that are not explicitly handled
        """
        # attempt to provide something; it will probably fail during configuration...
        return Default


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of MPI on macports machines, starting with
        the package the user has selected as the default
        """
        # on macports, mpi is a package group
        for package in macports.alternatives(group=cls.category):
            # if the package name starts with 'openmpi'
            if package.startswith(OpenMPI.flavor):
                # use OpenMPI
                factory = OpenMPI
            # if it starts with 'mpich'
            elif package.startswith(MPICH.flavor):
                # use MPICH
                factory = MPICH
            # otherwise
            else:
                # this is a bug...
                import journal
                # so complain
                raise journal.firewall('pyre.externals.MPI').log(
                    "unknown MPI flavor for package {!r}".format(package))
            # attempt to
            try:
                # instantiate the package and return it
                yield factory(name=package)
            # if this fails
            except factory.ConfigurationError:
                # try something else
                continue

        # if we get this far, try this
        yield cls.generic()

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure an MPI package instance on a macports host
        """
        # get the name of the {instance}
        name = instance.pyre_name
        # get the package group
        group = cls.category
        # ask macports for information about my category
        alternatives = macports.alternatives(group=group)
        # if the instance name is not one of the alternatives:
        if name not in alternatives:
            # go through what's there
            for alternative in alternatives:
                # and check whether any of them are implementations of my flavor
                if alternative.startswith(instance.flavor):
                    # set the target package name to this alternative
                    name = alternative
                    # and bail out
                    break
            # if we run out of options
            else:
                # this must be a poorly user configured instance; complain
                raise cls.ConfigurationError(
                    component=instance, errors=instance.pyre_configurationErrors)

        # get my selection info
        packageName, contents, smap = macports.getSelectionInfo(group=group, alternative=name)
        # get the version info
        version, variants = macports.info(package=packageName)

        # ask macports for its installation location
        prefix = macports.prefix()
        # find my {launcher}
        launcher = os.path.join(prefix, smap['bin/mpirun'])
        # extract my {bindir}
        bindir,_ = os.path.split(launcher)

        # the header regex
        header = "(?P<incdir>.*)/mpi.h$"
        # find the folder
        incdir = macports.incdir(regex=header, contents=contents)

        # find my library
        libmpi = "(?P<libdir>.*)/{}".format(cls.pyre_host.dynamicLibrary(group))
        # find the folder
        libdir = macports.libdir(regex=libmpi, contents=contents)

        # apply the configuration
        instance.version = version
        instance.prefix = prefix
        instance.bindir = bindir
        instance.incdir = incdir
        instance.libdir = libdir
        instance.launcher = launcher

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

        # if all else fails, go generic
        return cls.generic()


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
    flavor = "mpi"
    category = MPI.category

    # public state
    prefix = pyre.properties.str(default='/usr')
    prefix.doc = 'the package installation directory'

    bindir = pyre.properties.str(default='/usr/bin')
    bindir.doc = "the location of my binaries"

    incdir = pyre.properties.str(default='/usr/include')
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str(default='/usr/lib')
    libdir.doc = "the location of my libraries; for the linker command path"

    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'


# the openmpi package manager
class OpenMPI(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.mpi.openmpi', implements=MPI):
    """
    The package manager for OpenMPI packages
    """

    # constants
    flavor = "openmpi"
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
class MPICH(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.mpi.mpich', implements=MPI):
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
