# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import re, pathlib
# the framework
import pyre
# my protocol
from .PackageManager import PackageManager


# declaration
class Unmanaged(pyre.component, family='pyre.packagers.unmanaged', implements=PackageManager):
    """
    Support for un*x systems that don't have package management facilities
    """


    # constants
    name = 'bare'


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
    def configure(self, installation):
        """
        Dispatch to the {packageInstance} configuration procedure that is specific to a host
        without a specific package manager
        """
        # what she said...
        return installation.bare(manager=self)


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
            return pathlib.Path(match.group('path'))
        # otherwise, leave it blank
        return


    def locate(self, targets, paths):
        """
        Generate a sequence of the full {paths} to the {targets}
        """
        # go through the targets
        for target in targets:
            # and each of paths
            for path in paths:
                # form the combination
                candidate = path / target
                # check whether it exists
                if candidate.exists():
                    # got one
                    yield candidate
                    # grab the next
                    break
        # all done
        return


    # implementation details and support for my subclasses
    def getPrefix(self, default):
        """
        Identify the package manager install location
        """
        # check my cache
        prefix = self._prefix
        # for whether I have done this before
        if prefix is not None:
            # in which case I'm done
            return prefix
        # grab the shell utilities
        import shutil
        # locate the full path to the package manager client
        client = shutil.which(self.manager)
        # if we found it
        if client:
            # pathify
            client = pathlib.Path(client)
        # otherwise
        else:
            # maybe it's not on the path; try the default
            client = pathlib.Path(default) / self.manager
            # if it's not there
            if not client.exists():
                # build the message
                msg = 'could not locate {.manager!r}'.format(self)
                # complain
                raise self.ConfigurationError(configurable=self, errors=[msg])
            # found it; let's remember its location
            self.manager = client

        # extract the parent directory
        bin = client.parent
        # and once again to get the prefix
        prefix = bin.parent
        # set it
        self._prefix = prefix
        # and return it
        return prefix


# end of file
