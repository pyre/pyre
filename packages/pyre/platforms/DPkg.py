# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import re, subprocess
# framework
import pyre
# superclass
from .Unmanaged import Unmanaged


# declaration
class DPkg(Unmanaged, family='pyre.packagers.dpkg'):
    """
    Support for the debian package manager
    """


    # constants
    manager = 'dpkg-query'


    # interface obligations
    @pyre.export
    def prefix(self):
        """
        The location of installed packages
        """
        # always in the same spot
        return '/usr'


    @pyre.provides
    def installed(self):
        """
        Retrieve available information for all installed packages
        """
        # ask the index...
        return self.getInstalledPackages().items()


    @pyre.provides
    def choices(self, category):
        """
        Provide a sequence of package names that provide compatible installations for the given
        package {category}
        """
        # ask the package category to do dpkg specific hunting
        yield from category.dpkgChoices(dpkg=self)
        # all done
        return


    @pyre.export
    def info(self, package):
        """
        Return the available information about {package}
        """
        # send what is maintained by the index
        return self.getInstalledPackages()[package]


    @pyre.export
    def contents(self, package):
        """
        Retrieve the contents of the {package}
        """
        # ask port for the package contents
        yield from self.retrievePackageContents(package=package)
        # all done
        return


    @pyre.provides
    def configure(self, packageInstance):
        """
        Dispatch to the {packageInstance} configuration procedure that is specific to macports
        """
        # what she said...
        return packageInstance.dpkg(dpkg=self)


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
        Generate a sequence of all installed ports
        """
        # set up the shell command
        settings = {
            'executable': self.manager,
            'args': (self.manager, '--show'),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # and info parser
            info = self._infoParser
            # grab the rest
            for line in pipe.stdout.readlines():
                # parse
                match = info.match(line)
                # if it matched
                if match:
                    # extract the information we need and hand it to the caller
                    yield match.group('package', 'version', 'revision')
        # all done
        return


    def retrievePackageContents(self, package):
        """
        Generate a sequence of the contents of {package}
        """
        # set up the shell command
        settings = {
            'executable': self.manager,
            'args': (self.manager, '--listfiles', package),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # execute
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # grab the rest
            for line in pipe.stdout.readlines():
                # strip it and hand it to the caller
                yield line.strip()
        # all done
        return


    # private data
    _installed = None

    _infoParser = re.compile(
        r"(?P<package>[^\t]+)"
        r"\t"
        r"((?P<epoch>[\d]+):)?"
        r"(?P<version>[\w.+]+)"
        r"(-(?P<revision>[\w.+-]+))?"
        )


# end of file
