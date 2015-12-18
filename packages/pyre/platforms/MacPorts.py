# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, re, subprocess
# superclass
from .Darwin import Darwin


# declaration
class MacPorts(Darwin, family='pyre.platforms.macports'):
    """
    Encapsulation of a darwin host that runs macports
    """

    # constants
    manager = 'port'
    distribution = 'macports'


    # interface
    def installed(self, package):
        """
        Return the version and variants of the installed {package}
        """
        # grab the index
        installed = self._installed
        # if it has not been initialized
        if not installed:
            # build the installed package index
            installed = {
                package: (version, variants)
                for package, version, variants in self.installedPackages()
            }
            # attach it
            self._installed = installed
        # ask it
        return installed[package]


    def selected(self, group):
        """
        Return the selected package and all alternatives for the given package {group}
        """
        # grab the index
        selected = self._selected
        # if it has not been initialized
        if not selected:
            # build the selected package index
            selected = {
                group: (selection, alternatives)
                for group, selection, alternatives in self.selectedPackages()
            }
            # attach it
            self._selected = selected
        # ask it
        return selected[group]


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # empty out the indices
        self._selected = None
        self._installed = None
        # all done
        return


    # implementation details
    @classmethod
    def systemdirs(cls):
        """
        Generate a sequence of directories with system wide package installations
        """
        # first my prefix
        yield cls.prefix()
        # then whatever my ancestors have to say
        yield from super().systemdirs()
        # all done
        return


    @classmethod
    def prefix(cls):
        """
        The package manager install location
        """
        # check my cache
        prefix = cls._prefix
        # for whether I have done this before
        if prefix:
            # in which case I'm done
            return prefix
        # locate the full path to the port manager
        port = cls.which(cls.manager)
        # if not there
        if not port:
            # return an empty string
            return ''
        # otherwise, extract the directory with the tools
        bin, _ = os.path.split(port)
        # and finally the prefix
        prefix, _ = os.path.split(bin)
        # set it
        cls._prefix = prefix
        # and return it
        return prefix


    # package management
    @classmethod
    def installedPackages(cls, *packages):
        """
        Generate a sequence of all installed ports
        """
        # set up the shell command
        settings = {
            'executable': cls.manager,
            'args': (cls.manager, '-q', 'installed') + packages,
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
                # of this is not an active port
                if not status or status[0] != "(active)":
                    # skip it
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


    @classmethod
    def selectedPackages(cls, *groups):
        """
        Generate a sequence of alternatives for a particular port group
        """
        # template for the command line args
        # common settings for the shell command
        settings = {
            'executable': cls.manager,
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }

        # if we were not given any group names
        if not groups:
            # ask for a summary report
            settings['args'] = [ cls.manager, 'select', '--summary']
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
                    # hand to the caller
                    yield group, selection, set(alternatives.split())

            return

        # if we were given group names, set up the command line
        args = [ cls.manager, '-q', 'select' ]
        # iterate over all of them
        for group in groups:
            # ask for the current group
            settings['args'] = args + [group]
            # run the command
            with subprocess.Popen(**settings) as pipe:
                # reset the selection
                selection = 'none'
                # reset the alternatives
                alternatives = []
                # get the text source
                stream = pipe.stdout
                # grab the output
                for line in stream.readlines():
                    # strip it and split it
                    fields = line.strip().split()
                    # the package name is always an alternative, whether it is selected or not
                    alternatives.append(fields[0])
                    # if there is another field
                    if len(fields) > 1:
                        # if it is marked "active"
                        if fields[1] == "(active)":
                            # it is the selected package
                            selection = fields[0]
                # hand to the caller
                yield group, selection, set(alternatives)

        # all done
        return


    @classmethod
    def contents(cls, package):
        """
        Generate a sequence with the contents of {package}
        """
        # set up the shell command
        settings = {
            'executable': cls.manager,
            'args': (cls.manager, 'contents', package),
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


    @classmethod
    def selectionMap(cls, group, alternative):
        """
        Generate a map from {base} settings to the provided {alternative} for the given {group}
        """
        # get the folder with the group files
        folder = os.path.join(cls.prefix(), 'etc', 'select', group)
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


    @classmethod
    def provides(cls, filename):
        """
        Find the package that owns the given filename
        """
        # set up the shell command
        settings = {
            'executable': cls.manager,
            'args': (cls.manager, 'provides', filename),
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # grab the rest
            line = pipe.stdout.readline().strip()
            # check whether this filename belongs to a package
            match = cls._provides.match(line)
            # if it does
            if match:
                # extract the package name and return it
                return match.group('package')

        # if we got this far, we couldn't figure it out
        return


    @classmethod
    def provider(cls, group, alternative):
        """
        Identify the package in the {group} that provides the selected {alternative}
        """
        # get the selection map
        smap = cls.selectionMap(group=group, alternative=alternative)
        # form a filename that belongs to the target package
        filename = os.path.join(cls.prefix(), next(filter(None, smap.values())))
        # find out where it came from
        package = cls.provides(filename=filename)
        # get the package contents
        contents = tuple(cls.contents(package=package))
        # return the package, its contents, and the selection map
        return package, contents, smap


    # private data
    _prefix = None
    _provides = re.compile(r".* is provided by: (?P<package>.*)")


# end of file
