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


    # implementation details
    def installed(self):
        """
        Generate a sequence of all installed ports
        """
        # options
        settings = {
            'executable': self.manager,
            'args': [self.manager, 'installed'],
            'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # get the first line
            line = stream.readline().strip()
            # check it
            assert line == "The following ports are currently installed:"
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
                yield package, version, variants
        # all done
        return


    # implementation details
    _prefix = None


# end of file
