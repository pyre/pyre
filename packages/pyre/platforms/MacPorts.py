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
    Support for the macport package manager
    """


    # constants
    manager = 'port'


    # interface obligations
    @pyre.export
    def prefix(self):
        """
        The package manager install location
        """
        # ask port
        return self.getPrefix()


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
        yield from category.macportsChoices(macports=self)
        # all done
        return


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
        return selections.get(group, ())


    def getSelections(self):
        """
        Return the selected package and all alternatives for the given package {group}
        """
        # grab the index
        selections = self._selections
        # if it has not been initialized
        if selections is None:
            # build the selected package index
            selections = {
                group: alternatives
                for group, alternatives in self.retrieveSelectedPackages()
            }
            # attach it
            self._selections = selections
        # ask it
        return selections


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
            # grab each line
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


    def getSelectionInfo(self, group, alternative, smap=None):
        """
        Identify the package in the {group} that provides the selected {alternative}
        """
        # if we were not handed a specific selection map to use
        if smap is None:
            # get it
            smap = self.getSelectionMap(group=group, alternative=alternative)
        # form a filename that belongs to the target package
        filename = os.path.join(self.prefix(), next(filter(None, smap.values())))
        # find out where it came from
        package = self.getFileProvider(filename=filename)
        # return the package and the selection map
        return package


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
            # read a line and clean it up
            line = pipe.stdout.readline().strip()
            # check whether this filename belongs to a package
            match = self._provides.match(line)
            # if it does
            if match:
                # extract the package name and return it
                return match.group('package')

        # if we got this far, the filename does not belong to a package
        return


    def identifyPackage(self, package):
        """
        Attempt to map the {package} installation to the name of an installed package
        """
        # get the name of the {package} instance
        name = package.pyre_name
        # grab the index of installed packages
        installed = self.getInstalledPackages()

        # if {name} is the actual name of an installed package
        if name in installed:
            # we are done
            return name

        # another possibility is that {name} is one of the selection alternatives for a package
        # group; interpret the {package} category as the group name
        group = package.category
        # get the alternatives
        alternatives = self.alternatives(group=group)
        # and if we have a match
        if name in alternatives:
            # find which package provides it
            return self.getSelectionInfo(group=group, alternative=name)

        # another approach is to attempt to find a selection that is related to the package
        # flavor; let's check
        try:
            # whether the package has a flavor
            flavor = package.flavor
        # if it doesn't
        except AttributeError:
            # describe what went wrong
            msg = "could not deduce a package for {!r}".format(name)
            # and report it
            raise package.ConfigurationError(component=self, errors=[msg])

        # perhaps the flavor is the package name
        if flavor in installed:
            # in which case we are done
            return flavor

        # beyond this point, nothing works unless this package belongs to a selection group
        if not alternatives:
            # it isn't
            msg = 'could not locate a {.category!r} package for {!r}'.format(package, name)
            # so complain
            raise package.ConfigurationError(component=self, errors=[msg])

        # if has a flavor, collect all alternatives whose names start with the flavor
        candidates = [ tag for tag in alternatives if tag.startswith(flavor) ]

        # if there is exactly one candidate
        if len(candidates) == 1:
            # it's our best bet
            candidate = candidates[0]
            # find out which package implements it and return it
            return self.getSelectionInfo(group=group, alternative=candidate)

        # if there were no viable candidates
        if not candidates:
            # describe what went wrong
            msg = "no viable candidates for {.category!r}; please select one of {}".format(
                package, alternatives)
            # and report it
            raise package.ConfigurationError(component=self, errors=[msg])

        # otherwise, there were more than one candidate; describe what went wrong
        msg = 'multiple candidates for {!r}: {}; please select one'.format(
        flavor, candidates)
        # and report it
        raise package.ConfigurationError(component=self, errors=[msg])


    # private data
    # the root of the macports package library
    _prefix = None
    # the index of installed packages: (package name -> package info)
    _installed = None
    # the index of package groups: (package group -> tuple of alternatives)
    _selections = None
    # the parser of the macports response to provider queries
    _provides = re.compile(r".* is provided by: (?P<package>.*)")


# end of file
