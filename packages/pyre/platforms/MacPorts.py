# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, re, subprocess
# framework
import pyre
# superclass
from .Unmanaged import Unmanaged


# declaration
class MacPorts(Unmanaged, family='pyre.packagers.macports'):
    """
    Encapsulation of a host that uses macports as its package manager
    """


    # constants
    manager = 'port'
    distribution = 'macports'


    # interface obligations
    @pyre.export
    def prefix(self):
        """
        The package manager install location
        """
        # ask port
        return self.getPrefix()


    @pyre.export
    def info(self, package):
        """
        Return the available information about {package}
        """
        # send what the index has
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
        package {category}. MacPorts provides a way for the user to select a specific
        installation as the default, so it the default selection is the first package in the
        sequence.
        """
        # ask the package category to do macports specific hunting
        yield from category.macportsChooseImplementations(macports=self)
        # all done
        return


    @pyre.provides
    def configure(self, packageInstance):
        """
        Dispatch to the {packageInstance} configuration procedure that is specific to macports
        """
        # what she said...
        return packageInstance.macports(macports=self)


    # implementation details
    def getPrefix(self):
        """
        Identify the package manager install location
        """
        # check my cache
        prefix = self._prefix
        # for whether I have done this before
        if prefix is not None:
            # in which case I'm done
            return prefix
        # locate the full path to the port manager
        port = self.pyre_host.which(self.manager)
        # if there
        if not port:
            # maybe it's not on the path; try the default
            port = '/opt/local/bin/port'
            # if it's not there
            if not os.path.exists(port):
                # complain
                raise self.ConfigurationError('could not locate {.manager}'.format(self))
            # found it; let's remember its location
            self.manager = port

        # extract the directory with the tools
        bin, _ = os.path.split(port)
        # and now the prefix
        prefix, _ = os.path.split(bin)
        # set it
        self._prefix = prefix
        # and return it
        return prefix


    def getInstalledPackages(self):
        """
        Grant access to the installed package indexx
        """
        # grab the index
        installed = self._installed
        # if this the first time the index is accessed
        if installed is None:
            # prime it
            installed = {
                package: (version, variants)
                for package, version, variants in self.retrieveInstalledPackages()
            }
            # and attach it
            self._installed = installed
        # in any case, return it
        return installed


    def alternatives(self, group):
        """
        Generate a sequence of alternative installations for {group}, starting with the default
        selection
        """
        # grab the index
        selections = self.getSelections()
        # look up the given {group} and pass on the package alternatives
        return selections[group]


    def getSelections(self):
        """
        Return the selected package and all alternatives for the given package {group}
        """
        # grab the index
        selected = self._selected
        # if it has not been initialized
        if selected is None:
            # build the selected package index
            selected = {
                group: alternatives
                for group, alternatives in self.retrieveSelectedPackages()
            }
            # attach it
            self._selected = selected
        # ask it
        return selected


    def retrieveInstalledPackages(self):
        """
        Ask macports for installed package information
        """
        # set up the shell command
        settings = {
            'executable': self.manager,
            'args': (self.manager, '-q', 'installed', 'active'),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # grab the rest
            for line in stream.readlines():
                # strip it
                line = line.strip()
                # split on whitespace
                package, info, *status = line.split()
                # if this is not an active port
                if not status or status[0] != "(active)":
                    # this shouldn't happen, since we only asked for active ports; skip it
                    continue
                # unpack the info
                vinfo, *variants = info.split('+')
                # the version info starts with an @ sign
                assert vinfo[0] == '@'
                # and has two parts
                version, macrev = vinfo[1:].split('_')
                # hand it to the caller
                yield package, version, set(variants)
        # all done
        return


    def retrievePackageContents(self, package):
        """
        Generate a sequence with the contents of {package}
        """
        # set up the shell command
        settings = {
            'executable': self.manager,
            'args': (self.manager, 'contents', package),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # grab the rest
            for line in pipe.stdout.readlines():
                # strip it and hand it to the caller
                yield line.strip()
        # all done
        return


    def retrieveSelectedPackages(self):
        """
        Retrieve selection information for all known package groups
        """
        # template for the command line args
        settings = {
            'executable': self.manager,
            'args': ( self.manager, 'select', '--summary'),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }

        # run the command
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # the first two lines are headers; skip them
            next(stream)
            next(stream)
            # process the rest
            for line in stream:
                # strip, split, and unpack
                group, selection, alternatives = line.strip().split(maxsplit=2)
                # make a set out of the alternatives
                alternatives = list(alternatives.split())
                # remove the dummy marker 'none'; it should always be there
                alternatives.remove('none')

                # handle the selection: if it is 'none'
                if selection == 'none':
                    # it contributes nothing to the net alternatives
                    selection = []
                # if not
                else:
                    # remove it from the alternatives
                    alternatives.remove(selection)
                    # and put it at the top of the pile
                    selection = [selection]
                # turn the pile into a properly ordered tuple
                alternatives = tuple(selection + alternatives)
                # hand the pair to the caller
                yield group, alternatives

        # all done
        return


    def getSelectionInfo(self, group, alternative):
        """
        Identify the package in the {group} that provides the selected {alternative}
        """
        # get the selection map
        smap = self.getSelectionMap(group=group, alternative=alternative)
        # form a filename that belongs to the target package
        filename = os.path.join(self.prefix(), next(filter(None, smap.values())))
        # find out where it came from
        package = self.getFileProvider(filename=filename)
        # get the package contents
        contents = tuple(self.contents(package=package))
        # return the package, its contents, and the selection map
        return package, contents, smap


    def getSelectionMap(self, group, alternative):
        """
        Generate a map from {base} settings to the provided {alternative} for the given {group}
        """
        # get the folder with the group files
        folder = os.path.join(self.prefix(), 'etc', 'select', group)
        # if this is not a valid folder
        if not os.path.isdir(folder):
            # bail
            return {}
        # get the {base} file
        base = open(os.path.join(folder, 'base'))
        # and put its contents in a list
        keys = [ line.strip() for line in base.readlines() ]

        # get the file with the alternatives
        selection = open(os.path.join(folder, alternative))
        # and put its contents in a list
        values = [ line.strip() for line in selection.readlines() ]

        # build the map
        map = { base: value if value != '-' else None for base, value in zip(keys, values) }
        # and return it
        return map


    def getFileProvider(self, filename):
        """
        Find the package that owns the given filename
        """
        # set up the shell command
        settings = {
            'executable': self.manager,
            'args': (self.manager, 'provides', filename),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # grab the rest
            line = pipe.stdout.readline().strip()
            # check whether this filename belongs to a package
            match = self._provides.match(line)
            # if it does
            if match:
                # extract the package name and return it
                return match.group('package')

        # if we got this far, we couldn't figure it out
        return


    # private data
    _prefix = None
    _selected = None
    _installed = None
    _provides = re.compile(r".* is provided by: (?P<package>.*)")


# end of file
