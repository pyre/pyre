# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, glob
# framework
import pyre
# superclass
from .MPI import MPI


# the openmpi package manager
class OpenMPI(pyre.component, family='pyre.externals.openmpi', implements=MPI):
    """
    The package manager for OpenMPI packages
    """

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    bindir = pyre.properties.str()
    bindir.doc = "the location of my binaries"

    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"

    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'

    # constants
    category = MPI.category


    # framework hooks
    def pyre_configured(self):
        """
        Verify and correct the package configuration
        """
        # check in
        print("pyre.externals.OpenMPI.pyre_configured:")
        print("  host: {.pyre_host}".format(self))

        # do i need help?
        errors = tuple(self.checkConfiguration())
        # if there were no errors:
        if not errors:
            # move on
            print("  status: cool")
        # otherwise
        else:
            # complain
            print("  encountered the following errors:")
            for error in errors:
                print("    {}".format(error))

        # all done
        return


    # configuration validation
    def checkConfiguration(self):
        """
        Check that the MPI package instance is configured correctly
        """
        # check the location of the binaries
        yield from self.checkBindir()
        # check the location of the headers
        yield from self.checkIncdir()
        # check the location of the libraries
        yield from self.checkLibdir()
        # all done
        return


    def checkBindir(self):
        """
        Verify that the path to my binaries is set, exists, and contains what i expect
        """
        # get the setting
        bindir = self.bindir
        # check there is a value
        if not bindir:
            # complain
            yield "no 'bindir' setting"
            # and stop
            return
        # check that it is a valid directory
        if not os.path.isdir(bindir):
            # complain
            yield "{!r} is not a valid directory".format(bindir)
            # and stop
            return

        # at the very least, my launcher should be there
        launcher = os.path.join(bindir, self.launcher)
        # check
        if not os.path.exists(launcher):
            # complain
            yield "couldn't locate {.launcher!r} in {}".format(self, bindir)
            # and stop
            return

        # NYI: some installations make symbolic links in order to support alternatives; it
        # would be nice to check that if the launcher is a link, it point to my launcher, not
        # to one belonging to some other installation

        # if we made it this far, all is good
        return


    def checkIncdir(self):
        """
        Verify that the path to my headers is set, exists, and contains what i expect
        """
        # get the setting
        incdir = self.incdir
        # check there is a value
        if not incdir:
            # complain
            yield "no 'incdir' setting"
            # and stop
            return
        # check that it is a valid directory
        if not os.path.isdir(incdir):
            # complain
            yield "{!r} is not a valid directory".format(incdir)
            # and stop
            return

        # at the very least, my master header file
        header = "mpi.h"
        # should be there
        master = os.path.join(incdir, header)
        # check
        if not os.path.exists(master):
            # complain
            yield "couldn't find {!r} in {}".format(header, incdir)
            # and stop
            return

        # if we made it this far, all is good
        return



    def checkLibdir(self):
        """
        Verify that the path to my headers is set, exists, and contains what i expect
        """
        # get the setting
        libdir = self.libdir
        # check there is a value
        if not libdir:
            # complain
            yield "no 'libdir' setting"
            # and stop
            return
        # check that it is a valid directory
        if not os.path.isdir(libdir):
            # complain
            yield "{!r} is not a valid directory".format(libdir)
            # and stop
            return

        # at the very least, my library
        library = "libmpi.*"
        # should be there
        master = os.path.join(libdir, library)
        # expand
        candidates = glob.glob(master)
        # check
        if not candidates:
            # complain
            yield "could not find {!r} in {}".format(library, libdir)
            # and stop
            return

        # if we made it this far, all is good
        return


# end of file
