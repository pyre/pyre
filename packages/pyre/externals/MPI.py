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
    def generic(cls, host):
        """
        Provide a default implementation of MPI on platforms that are not explicitly handled
        """
        # print("    going generic")
        # attempt to provide something; it will probably fail during configuration...
        from .GenericMPI import GenericMPI
        # and return it
        return GenericMPI


    @classmethod
    def macports(cls, host):
        """
        Identify the default implementation of MPI on macports machines
        """
        # this is a macports host; ask it for the selected mpi package
        selection, alternatives = host.selected(cls.category)
        # show me
        # print("    selection: {!r}".format(selection))
        # print("    alternatives: {}".format(alternatives))

        # try to identify the selected port, hence the one the user considers the default on
        # this host

        # if the selection is an openmpi variant
        if selection.startswith('openmpi'):
            # show me
            # print("    using the selected 'openmpi' installation: {!r}".format(selection))
            # get the support for OpenMPI
            from .OpenMPI import OpenMPI
            # and return it
            return OpenMPI(name=selection)
        # if the selection is an mpich variant
        if selection.startswith('mpich'):
            # show me
            # print("    using the selected 'mpich' installation: {!r}".format(selection))
            # get the support for MPICH
            from .MPICH import MPICH
            # and return it
            return MPICH(name=selection)

        # nothing useful selected; let's look through the installed packages for openmpi
        for alternative in alternatives:
            # get the support for OpenMPI
            from .OpenMPI import OpenMPI
            # if the name starts with openmpi
            if alternative.startswith('openmpi'):
                # attempt to
                try:
                    # show me
                    # print("    attempting to use the alternative {!r}".format(alternative))
                    # instantiate it and return it
                    return OpenMPI(name=alternative)
                # if it couldn't be configured properly
                except OpenMPI.ConfigurationError:
                    # carry on
                    continue

        # nothing useful selected; let's look through the installed packages for openmpi
        for alternative in alternatives:
            # get the support for MPICH
            from .MPICH import MPICH
            # if the name starts with openmpi
            if alternative.startswith('mpich'):
                # attempt to
                try:
                    # show me
                    # print("    attempting to use the alternative {!r}".format(alternative))
                    # instantiate it and return it
                    return MPICH(name=alternative)
                # if it couldn't be configured properly
                except MPICH.ConfigurationError:
                    # carry on
                    continue

        # if we get this far, not much else to do
        return cls.generic(host=host)


    @classmethod
    def macportsConfigureInstance(cls, package, host):
        """
        Configure an MPI package instance on a macports host
        """
        # ask the package manager for its installation location
        prefix = host.prefix()
        # ask the package manager for information about my category
        selection, alternatives = host.selected(cls.category)
        # get my name
        name = package.pyre_name
        # if my name is not one of the alternatives:
        if name not in alternatives:
            # go through what's there
            for alternative in alternatives:
                # and check whether any of them are implementations of my flavor
                if alternative.startswith(package.flavor):
                    # set the target package name to this alternative
                    name = alternative
                    # and bail out
                    break
            # if we run out of options
            else:
                # this must be a poorly user configured instance; complain
                raise cls.ConfigurationError(
                    component=package, errors=package.pyre_configurationErrors)

        # get my selection info
        packageName, contents, smap = host.provider(group=cls.category, alternative=name)

        # find my {launcher}
        launcher = os.path.join(prefix, smap['bin/mpirun'])
        # extract my {bindir}
        bindir,_ = os.path.split(launcher)

        # find my header
        header = "mpi.h"
        # search for it in contents
        for path in contents:
            # split it
            folder, filename = os.path.split(path)
            # if the filename is a match
            if filename == header:
                # save the folder
                incdir = folder
                # and bail
                break
        # otherwise
        else:
            # leave it blank; we will complain below
            incdir = ''

        # find my library
        libmpi = host.dynamicLibrary('mpi')
        # search for it in contents
        for path in contents:
            # split it
            folder, filename = os.path.split(path)
            # if the filename is a match
            if filename == libmpi:
                # save the folder
                libdir = folder
                # and bail
                break
        # otherwise
        else:
            # leave it blank; we will complain below
            libdir = ''

        # apply the configuration
        package.prefix = prefix
        package.bindir = bindir
        package.incdir = incdir
        package.libdir = libdir
        package.launcher = launcher

        # all done
        return


# end of file
