# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re
import subprocess

# framework
import pyre

# superclass
from .Managed import Managed


# declaration
class DPkg(Managed, family="pyre.platforms.packagers.dpkg"):
    """
    Support for the debian package manager
    """

    # constants
    name = "dpkg"
    client = "dpkg-query"
    defaultLocation = pyre.primitives.path("/usr/bin")

    # implementation details
    def getInstalledPackages(self):
        """
        Return the version and revision of all installed packages
        """
        # grab the index
        installed = self._installed
        # if it has not been initialized
        if installed is None:
            # prime it
            installed = {
                package: (version, revision)
                for package, version, revision in self.retrieveInstalledPackages()
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
                "--show",
                "--showformat=${binary:Package}\t${Version}\t${db:Status-Abbrev}\n",
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
            # and info parser
            info = self._infoParser
            # grab the rest
            for line in stream.readlines():
                # parse
                match = info.match(line)
                # if it matched
                if match:
                    # extract the information we need and hand it to the caller
                    yield match.group("package", "version", "revision")
        # all done
        return

    def retrievePackageContents(self, package):
        """
        Generate a sequence of the contents of {package}
        """
        # set up the shell command
        settings = {
            "executable": str(self.client),
            "args": (str(self.client), "--listfiles", package),
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

    _infoParser = re.compile(
        r"(?P<package>[^\t:]+)(?P<arch>[^\t]+)?"
        r"\t"
        r"((?P<epoch>[\d]+):)?"
        r"(?P<version>[\w.+]+)"
        r"((?P<revision>[\w.+~-]+))?"
        r"\tii"
    )


# end of file
