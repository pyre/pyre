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

        # otherwise, we are on a single core host
        return ids, ids


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
