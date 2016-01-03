# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import re, collections, pathlib, subprocess
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
    name = 'macports'
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
        installation as the default, so the default selection is the first package in the
        sequence.
        """
        # check whether this package category can interact with me
        try:
            # by looking for my handler
            choices = category.macportsChoices
        # if it can't
        except AttributeError:
            # the error message template
            template = "the package {.category!r} does not support {.name!r}"
            # build the message
            msg = template.format(category, self)
            # complain
            raise self.ConfigurationError(configurable=self, errors=[msg])

        # otherwise, ask the package category to do macports specific hunting
        yield from choices(macports=self)

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
    def configure(self, installation):
        """
        Dispatch to the {installation} configuration procedure that is specific to macports
        """
        # what she said...
        return installation.macports(macports=self)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my normalization map
        self._normalizations = collections.defaultdict(dict)
        # all done
        return


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
        # if not there
        if not port:
            # maybe it's not on the path; try the default
            port = pathlib.Path('/opt/local/bin/port')
            # if it's not there
            if not port.exists():
                # build the message
                msg = 'could not locate {.manager}'.format(self)
                # complain
                raise self.ConfigurationError(configurable=self, errors=[msg])
            # found it; let's remember its location
            self.manager = port
        # otherwise
        else:
            # pathify
            port = pathlib.Path(port)


        # extract the directory with the tools
        bin = port.parent
        # and now the prefix
        prefix = bin.parent
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
        alternatives = self.getAlternatives()
        # look up the given {group} and pass on the package alternatives
        return alternatives.get(group, ())


    def getAlternatives(self):
        """
        Return the selected package and all alternatives for the given package {group}
        """
        # grab the index
        alternatives = self._alternatives
        # if it has not been initialized
        if alternatives is None:
            # build the selected package index
            alternatives = {
                group: candidates
                for group, candidates in self.retrievePackageAlternatives()
            }
            # attach it
            self._alternatives = alternatives
        # ask it
        return alternatives


    def retrieveInstalledPackages(self):
        """
        Ask macports for installed package information
        """
        # set up the shell command
        settings = {
            'executable': str(self.manager),
            'args': (str(self.manager), '-q', 'installed', 'active'),
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
            'executable': str(self.manager),
            'args': (str(self.manager), 'contents', package),
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


    def retrievePackageAlternatives(self):
        """
        Retrieve selection information for all known package groups
        """
        # template for the command line args
        settings = {
            'executable': str(self.manager),
            'args': ( str(self.manager), 'select', '--summary'),
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
        # get the package normalization map
        _, target = self.getNormalization(group=group, alternative=alternative)
        # form a filename that belongs to the target package
        filename = self.prefix() / target[0]
        # find out where it came from
        package = self.getFileProvider(filename=filename)
        # return the package and the selection map
        return package


    def getNormalization(self, group, alternative):
        """
        Retrieve the normalization map for {alternative} from {group}
        """
        # get the table for {group}
        table = self._normalizations[group]

        # attempt to
        try:
            # get the canonical filenames from 'base'
            base = table['base']
        # if its not there
        except KeyError:
            # pull in the sequence of files from 'base'
            base = tuple(self.retrieveNormalizationTable(group=group, alternative='base'))
            # record it for next time
            table['base'] = base

        # next, attempt to
        try:
            # get the sequence of files from alternative
            target = table[alternative]
        # if not there
        except KeyError:
            # pull in the list of files from {alternative}
            target = tuple(self.retrieveNormalizationTable(group=group, alternative=alternative))
            # record it
            table[alternative] = target

        # return the pair
        return base, target


    def retrieveNormalizationTable(self, group, alternative):
        """
        Populate the {group} normalization table with the selections for {alternative}
        """
        # form the filename
        name = self.prefix() / 'etc' / 'select' / group / alternative
        # open it
        with name.open() as stream:
            # pull the contents
            for line in stream.readlines():
                # strip
                line = line.strip()
                # interpret it and pass it on
                yield pathlib.Path(line) if line != '-' else None
        # all done
        return


    def getFileProvider(self, filename):
        """
        Find the package that owns the given filename
        """
        # set up the shell command
        settings = {
            'executable': str(self.manager),
            'args': (str(self.manager), 'provides', str(filename)),
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


    def identify(self, installation):
        """
        Attempt to map the package {installation} to the name of an installed package
        """
        # get the name of the {installation} instance
        name = installation.pyre_name
        # grab the index of installed packages
        installed = self.getInstalledPackages()

        # if {name} is the actual name of an installed package
        if name in installed:
            # we are done
            return name

        # another possibility is that {name} is one of the selection alternatives for a package
        # group; interpret the {installation} category as the group name
        group = installation.category
        # get the alternatives
        alternatives = self.alternatives(group=group)
        # and if we have a match
        if name in alternatives:
            # find which package provides it
            return self.getSelectionInfo(group=group, alternative=name)

        # another approach is to attempt to find a selection that is related to the package
        # flavor; let's check
        try:
            # whether the installation has a flavor
            flavor = installation.flavor
        # if it doesn't
        except AttributeError:
            # describe what went wrong
            msg = "could not find a package installation for {!r}".format(name)
            # clear any previous configuration errors; they are now irrelevant
            installation.pyre_configurationErrors = []
            # and report it
            raise package.ConfigurationError(configurable=self, errors=[msg])

        # perhaps the flavor is the package name
        if flavor in installed:
            # in which case we are done
            return flavor

        # beyond this point, nothing works unless this package belongs to a selection group
        if not alternatives:
            # it isn't
            msg = 'could not locate a {.category!r} package for {!r}'.format(installation, name)
            # clear any previous configuration errors; they are now irrelevant
            installation.pyre_configurationErrors = []
            # complain
            raise installation.ConfigurationError(configurable=self, errors=[msg])

        # collect all alternatives whose names start with the flavor
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
                installation, alternatives)
            # clear any previous configuration errors; they are now irrelevant
            installation.pyre_configurationErrors = []
            # and report it
            raise installation.ConfigurationError(configurable=self, errors=[msg])

        # otherwise, there were more than one candidate; describe what went wrong
        msg = 'multiple candidates for {!r}: {}; please select one'.format(flavor, candidates)
        # clear any previous configuration errors; they are now irrelevant
        installation.pyre_configurationErrors = []
        # and report it
        raise installation.ConfigurationError(configurable=self, errors=[msg])


    # private data
    # the root of the macports package library
    _prefix = None
    # the index of installed packages: (package name -> package info)
    _installed = None
    # the index of package groups: (package group -> tuple of alternatives)
    _alternatives = None

    # the table of package normalizations; this is a map from a selection group to a another
    # map, one that takes alternatives to the list of files they replace; the canonical package
    # interface is provided by the special key 'base'
    _normalizations = None

    # the parser of the macports response to provider queries
    _provides = re.compile(r".* is provided by: (?P<package>.*)")


# end of file
