# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import operator
import collections
# superclass
from .Platform import Platform


# declaration
class Linux(Platform, family='pyre.hosts.linux'):
    """
    Encapsulation of a generic linux host
    """


    # public data
    platform = 'linux'


    # implementation details: explorers
    @classmethod
    def cpuServey(cls):
        """
        Collect information about the CPU resources on this host
        """
        # initialize the cpu store
        cpus = collections.defaultdict(dict)
        # the marker
        physicalid = None
        # prime the tokenizer
        tokens = cls.tokenizeCPUInfo()
        # the keys we car about
        targets = {'siblings', 'cpu cores'}
        # parse
        for key, value in tokens:
            # if the key is blank, reset the marker
            if not key: physicalid = None
            # harvest the cpu physical id
            if key == 'physical id': physicalid = value
            # harvest the interesting info
            if key in targets: cpus[physicalid][key] = value

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
        
        # that's all for now
        return physical, logical


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
    cpuinfo = '/proc/cpuinfo'


# end of file 
