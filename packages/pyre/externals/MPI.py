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
        from .GenericMPI import GenericMPI
        # and return it
        return GenericMPI


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of MPI on macports machines, starting with
        the package the user has selected as the default
        """
        # get the MPI implementations known to macports
        from .MPICH import MPICH as mpich
        from .OpenMPI import OpenMPI as openmpi

        # on macports, mpi is a package group
        for package in macports.alternatives(group=cls.category):
            # if the package name starts with 'openmpi'
            if package.startswith(openmpi.flavor):
                # use OpenMPI
                factory = openmpi
            # if it starts with 'mpich'
            elif package.startswith(mpich.flavor):
                # use MPICH
                factory = mpich
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
        # get the package group
        group = cls.category
        # ask the package manager for information about my category
        alternatives = macports.alternatives(group=group)
        # get my name
        name = instance.pyre_name
        # if my name is not one of the alternatives:
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


# end of file
