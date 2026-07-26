# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import subprocess

# framework
import pyre

# superclass
from .Managed import Managed


# declaration
class Rpm(Managed, family="pyre.platforms.packagers.rpm"):
    """
    Support for the rpm package manager

    The primitives are {rpm} itself, the stable substrate beneath yum, dnf, and dnf5, so the
    engine works unchanged across the fedora/rhel family
    """

    # constants
    name = "rpm"
    client = "rpm"
    defaultLocation = pyre.primitives.path("/usr/sbin")

    # implementation details
    def getInstalledPackages(self):
        """
        Return the version and release of all installed packages
        """
        # grab the index
        installed = self._installed
        # if it has not been initialized
        if installed is None:
            # prime it
            installed = {
                package: (version, release)
                for package, version, release in self.retrieveInstalledPackages()
            }
            # attach it
            self._installed = installed
        # ask it
        return installed

    def retrieveInstalledPackages(self):
        """
        Generate a sequence of all installed packages
        """
        # set up the shell command
        settings = {
            "executable": str(self.client),
            "args": (
                str(self.client),
                "-qa",
                "--queryformat",
                "%{NAME}\t%{VERSION}\t%{RELEASE}\n",
            ),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # grab each line
            for line in stream.readlines():
                # take it apart
                fields = line.strip().split("\t")
                # skip malformed lines
                if len(fields) != 3:
                    # and move on
                    continue
                # unpack
                package, version, release = fields
                # hand the triplet to the caller
                yield package, version, release
        # all done
        return

    def retrievePackageContents(self, package):
        """
        Generate a sequence of the contents of {package}
        """
        # set up the shell command
        settings = {
            "executable": str(self.client),
            "args": (str(self.client), "-ql", package),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # execute
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # grab the rest
            for line in stream.readlines():
                # strip it and hand it to the caller
                yield line.strip()
        # all done
        return

    # private data
    _installed = None


# end of file
