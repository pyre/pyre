# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import platform
# framework
import pyre
# my protocol
from .Platform import Platform


# declaration
class Host(pyre.component, family='pyre.platforms.generic', implements=Platform):
    """
    Encapsulation of a generic host
    """

    # public data
    # host
    hostname = platform.node() # the name of the host on which this process is running
    nickname = None # the short name assigned to this host by the user
    # cpus
    cpus = None # the triplet (cpus, physical cores, logical cores)
    # os
    platform = None # the OS type on which this process is running
    release = None # the OS release
    codename = None # the OS version
    # distribution
    distribution = None # a clue about the package manager on this machine

    # user configurable state
    externals = pyre.externals.catalog()
    externals.doc = 'the database of external packages installed on this host'


    # protocol obligations
    @classmethod
    def flavor(cls):
        """
        Return a suitable default encapsulation of the runtime host
        """
        # the default; override in subclasses
        return cls


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # discover the number of cpus
        self.cpus = self.cpuSurvey()
        # all done
        return


    # implementation details: explorers
    @classmethod
    def cpuSurvey(cls):
        """
        Collect information about the CPU resources on this host
        """
        # by default, we know nothing; so assume one single core cpu with no hyper-threading
        # subclasses should override with their platform dependent survey code
        return (1,1)


# end of file 
