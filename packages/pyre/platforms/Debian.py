# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import re, subprocess
# superclass
from .Linux import Linux


# declaration
class Debian(Linux, family='pyre.platforms.debian'):
    """
    Encapsulation of a host running linux on the ubuntu distribution
    """

    # constants
    manager = 'dpkg-query'
    distribution = 'debian'


    # implementation details
    @classmethod
    def installed(cls, *packages):
        """
        Generate a sequence of all installed ports
        """
        # set up the shell command
        settings = {
            'executable': cls.manager,
            'args': (cls.manager, '--show') + packages,
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
                # parse
                match = cls.regex.match(line)
                # if it matched
                if match:
                    # extract the information we need
                    package, version, revision = match.group('package', 'version', 'revision')
                    # hand it to the caller
                    yield package, version, revision
        # all done
        return


    # private data
    regex = re.compile(
        r"(?P<package>[^\t]+)"
        r"\t"
        r"((?P<epoch>[\d]+):)?"
        r"(?P<version>[\w.+]+)"
        r"(-(?P<revision>[\w.+-]+))?"
        )


# end of file
