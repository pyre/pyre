# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import re
import sys
import pyre # the framework
import platform
# my interface
from .Shell import Shell as shell


# declaration
class Executive(pyre.component, implements=shell):
    """
    The base class for hosting strategies
    """


    # user configurable state
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"

    hostmap = pyre.map(cast=pyre.properties.str)
    hostmap.doc = """
        a mapping of host nicknames to regular expressions that match against the formal
        machine name as returned by platform.uname()
        """

    # public data
    system = None # the type of host on which this process is running
    release = None # the OS release
    version = None # the OS version
    architecture = None # the CPU architecture
    processor = None # the CPU type

    hostname = None # the name of the host on which this process is running
    nickname = None # the nickname of the host on which this process is running
    platform = None # the OS type on which this process is running


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior
        """
        # {Executive} is abstract
        raise NotImplementedError("class {.__name__} must implement 'launch'".format(type(self)))


    def loadHostConfiguration(self, name=None):
        """
        Load the configuration files for the named host
        """


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # host discovery
        (system, name, release, version, architecture, processor) = platform.uname()
        self.hostname = self.nickname = name
        self.system = system
        self.release = release
        self.version = version
        self.architecture = architecture
        self.processor = processor
        
        self.platform = sys.platform

        # check whether we know this host by a nickname by looking through my {hostmap}
        for nickname, regex in self.hostmap.items():
            # if the hostname matches
            if re.match(regex, name):
                # set the nickname
                self.nickname = nickname
                # all done
                break

        # all done
        return


# end of file 
