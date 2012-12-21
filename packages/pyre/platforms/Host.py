# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    hostname = None # the name of the host on which this process is running
    nickname = None # the short name assigned to this host by the user
    platform = None # the OS type on which this process is running
    
    system = None # the type of host on which this process is running
    release = None # the OS release
    version = None # the OS version
    architecture = None # the CPU architecture
    processor = None # the CPU type

    cpus = None # the triplet (cpus, physical cores, logical cores)


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
        self.cpus = self.cpuServey()
        return


    # implementation details: explorers
    @classmethod
    def cpuServey(cls):
        """
        Collect information about the CPU resources on this host
        """
        raise NotImplementedError("class {.__name__!r} must implement 'cpuServey'".format(cls))


# end of file 
