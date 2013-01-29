# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# framework
import pyre
# my protocol
from .Platform import Platform


# declaration
class Host(pyre.component, implements=Platform):
    """
    Encapsulation of a generic linux host
    """

    # public data
    # host
    hostname = None # the name of the host on which this process is running
    nickname = None # the short name assigned to this host by the user
    # cpus
    cpus = None # the triplet (cpus, physical cores, logical cores)
    # os
    platform = None # the OS type on which this process is running
    release = None # the OS release
    codename = None # the OS version
    # distribution
    distribution = None # a clue about the package manager on this machine


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

        # get the python platform package
        import platform
        # set the hostname
        self.hostname = platform.node()
        # discover the number of cpus
        self.cpus = self.cpuSurvey()

        return


    # implementation details: explorers
    @classmethod
    def cpuSurvey(cls):
        """
        Collect information about the CPU resources on this host
        """
        raise NotImplementedError("class {.__name__!r} must implement 'cpuSurvey'".format(cls))


# end of file 
