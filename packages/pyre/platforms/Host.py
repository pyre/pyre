# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import platform
import socket
# framework
import pyre
# my protocol
from .Platform import Platform
# info
from .CPUInfo import CPUInfo
from .MemoryInfo import MemoryInfo


# declaration
class Host(pyre.component, family='pyre.platforms.generic', implements=Platform):
    """
    Encapsulation of a generic host
    """

    # public data
    # host
    fqdn = socket.getfqdn()    # the fully qualifies domain name, if available
    hostname = platform.node() # the name of the host on which this process is running
    nickname = None            # the short name assigned to this host by the user
    # os
    platform = None            # the OS type on which this process is running
    release = None             # the OS release
    codename = None            # the OS version
    # distribution
    distribution = None        # a clue about the package manager on this machine

    @property
    def cpus(self):
        """
        The CPU configuration of the machine as a triplet (cpus, physical cores, logical cores)
        """
        # if we haven't done this before
        if self._cpus is None:
            # find out
            self._cpus = self.cpuSurvey()
        # all done
        return self._cpus

    @property
    def memory(self):
        """
        Information about the memory on the host
        """
        # do not cache anything, to make sure the information we return is always up to date
        return self.memorySurvey()

    @property
    def tag(self):
        """
        Build a tag for this host that pairs the platform name with the cpu architecture
        """
        # easy enough
        return f"{self.platform}-{self.cpus.architecture}"

    # user configurable state
    externals = pyre.properties.dict(schema=pyre.properties.str())
    externals.doc = 'a map of package categories to installation instances'

    packager = pyre.platforms.packager()
    packager.doc = 'the manager of external packages installed on this host'


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the CPU info cache
        self._cpus = None
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
        return CPUInfo()


    @classmethod
    def memorySurvey(cls):
        """
        Collect information about the memory on this host
        """
        # by default, we know nothing
        # subclasses should override with their platform dependent survey code
        return MemoryInfo()


    # feature support
    @classmethod
    def dynamicLibrary(cls, stem):
        """
        Convert the sequence of stems into likely filenames for shared objects
        """
        # go through each one
        return cls.template_dynamicLibrary.format(cls, stem)


    @classmethod
    def staticLibrary(cls, stem):
        """
        Convert the sequence of stems into likely filenames for shared objects
        """
        # go through each one
        return cls.template_staticLibrary.format(cls, stem)


    @classmethod
    def dynamicLibraries(cls, stems):
        """
        Convert the sequence of stems into likely filenames for shared objects
        """
        # go through each one
        return (cls.template_dynamicLibrary.format(cls, stem) for stem in stems)


    @classmethod
    def staticLibraries(cls, stems):
        """
        Convert the sequence of stems into likely filenames for shared objects
        """
        # go through each one
        return (cls.template_staticLibrary.format(cls, stem) for stem in stems)


# end of file
