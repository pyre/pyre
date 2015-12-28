# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import re
# the framework
import pyre
# my protocol
from .PackageManager import PackageManager


# declaration
class Unmanaged(pyre.component, family='pyre.packagers.unmanaged', implements=PackageManager):
    """
    Support for un*x systems that don't have package management facilities
    """


    # protocol obligations
    @pyre.export
    def prefix(self):
        """
        The package manager install location
        """
        # don't have one
        return ''


    @pyre.export
    def installed(self):
        """
        Retrieve available information for all installed packages
        """
        # don't have any
        return ()


    @pyre.provides
    def choices(self, category):
        """
        Provide a sequence of package names that provide compatible installations for the given
        package {category}.
        """
        # don't have any
        return ()


    @pyre.export
    def info(self, package):
        """
        Return information about the given {package}
        """
        # don't know anything
        raise KeyError(package)

    @pyre.export
    def contents(self, package):
        """
        Generate a sequence of the contents of the {package}
        """
        # don't know anything
        raise KeyError(package)


    @pyre.provides
    def configure(self, packageInstance):
        """
        Dispatch to the {packageInstance} configuration procedure that is specific to a host
        without a specific package manager
        """
        # what she said...
        return packageInstance.unmanaged(manager=self)


    # interface
    def find(self, target, pile):
        """
        Interpret {target} as a regular expression and return a sequence of the contents of {pile}
        that match it.

        This is intended as a way to scan through the contents of packages to find a path that
        matches {target}
        """
        # compile the target regex
        regex = re.compile(target)

        # go through the pile
        for item in pile:
            # check
            match = regex.match(item)
            # if it matches
            if match:
                # hand it to the caller
                yield match

        # all done
        return


    def findfirst(self, target, contents):
        """
        Locate the path to {target} in the {contents} of some package
        """
        # form the regex
        regex = '(?P<path>.*)/{}$'.format(target)
        # search for it in contents
        for match in self.find(target=regex, pile=contents):
            # extract the folder
            return match.group('path')
        # otherwise, leave it blank
        return ''


# end of file
