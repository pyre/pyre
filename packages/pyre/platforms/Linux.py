# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import collections, operator
# superclass
from .POSIX import POSIX


# declaration
class Linux(POSIX, family='pyre.platforms.linux'):
    """
    Encapsulation of a generic linux host
    """


    # public data
    platform = 'linux'
    distribution = 'generic'

    prefix_library = 'lib'
    extension_staticLibrary = '.a'
    extension_dynamicLibrary = '.so'

    template_staticLibrary = "{0.prefix_library}{1}{0.extension_staticLibrary}"
    template_dynamicLibrary = "{0.prefix_library}{1}{0.extension_dynamicLibrary}"


    # protocol obligations
    @classmethod
    def flavor(cls):
        """
        Return a suitable default encapsulation of the runtime host
        """
        # get the platform package
        import platform
        # identify the platform characteristics; careful not to set the {distribution}
        # attribute here; the subclasses set the distribution name to the pyre canonical
        # nickname
        distribution, cls.release, cls.codename = platform.linux_distribution()

        # check for ubuntu
        if distribution.lower().startswith('ubuntu'):
            # load the platform file
            from .Ubuntu import Ubuntu
            # and return it
            return Ubuntu
        if distribution.lower().startswith('debian'):
            # load the platform file
            from .Debian import Debian
            # and return it
            return Debian
        # check for red hat
        if distribution.lower().startswith('red hat'):
            # load the platform file
            from .RedHat import RedHat
            # and return it
            return RedHat
        # check for centos
        if distribution.lower().startswith('centos'):
            # load the platform file
            from .CentOS import CentOS
            # and return it
            return CentOS

        # otherwise, act like a generic linux system
        return cls


    # implementation details: explorers
    @classmethod
    def cpuSurvey(cls):
        """
        Collect information about the CPU resources on this host
        """
        # initialize the cpu store
        ids = 0
        cpus = collections.defaultdict(dict)
        # the markers
        physicalid = None
        # prime the tokenizer
        tokens = cls.tokenizeCPUInfo()
        # the keys we care about
        targets = {'siblings', 'cpu cores'}
        # parse
        for key, value in tokens:
            # if the key is blank
            if not key:
                # reset the marker
                physicalid = None
                # and move on
                continue
            # record the processor ids; that's all we have on single core machines
            if key == 'processor':
                # increment the count
                ids += 1
                # move on
                continue
            # the socket to which this core belongs
            if key == 'physical id':
                # harvest the cpu physical id
                physicalid = value
                # move on
                continue
            # harvest the interesting info
            if physicalid and key in targets:
                # attach it to the right socket
                cpus[physicalid][key] = value
                # and move on
                continue

        # initialize the counters
        sockets = physical = logical = 0
        # reduce
        for info in cpus.values():
            # update the cpu count
            sockets += 1
            # update the number of physical cores
            physical += int(info['cpu cores'])
            # update the number of logical cores
            logical += int(info['siblings'])

        # if the reduction produced non-zero results
        if physical and logical:
            # that's all for now
            return physical, logical

        # otherwise, punt
        return super().cpuSurvey()


    # implementation details: workhorses
    @classmethod
    def tokenizeCPUInfo(cls):
        """
        Split the CPU info file into (key, value) pairs
        """
        # on linux, all the info is in '/proc/cpuinfo'
        with open(cls.cpuinfo) as cpuinfo:
            # in order to tokenize each line
            for line in cpuinfo:
                # strip whitespace
                line = line.strip()
                # if this leaves us with nothing, we ran into a separator blank line
                if not line:
                    # form a pair of blank tokens
                    key = value = ''
                # otherwise
                else:
                    # split apart and strip leading and trailing whitespace
                    key, value = map(operator.methodcaller('strip'), line.split(':'))
                # yield the tokens
                yield key, value
        # nothing more
        return


    # implementation constants
    issue = '/etc/issue'
    cpuinfo = '/proc/cpuinfo'


# end of file
