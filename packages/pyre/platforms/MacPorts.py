# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, subprocess
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
    def installed(cls, *packages):
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
            for line in pipe.stdout.readlines():
                # strip it
                line = line.strip()
                # split on whitespace
                package, info, status = line.split()
                # of this is not an active port
                if status != "(active)":
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
    def selected(cls, *groups):
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


    # implementation details
    _prefix = None


# end of file
