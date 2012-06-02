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
import operator
import platform
# my interface
from .Shell import Shell as shell


# declaration
class Executive(pyre.component, family='pyre.shells.executive', implements=shell):
    """
    The base class for hosting strategies
    """


    # constants
    # the key under which users can specify nicknames for known hosts
    hostmapkey = ['pyre', 'hostmap']

    # user configurable state
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"

    # public data
    system = None # the type of host on which this process is running
    release = None # the OS release
    version = None # the OS version
    architecture = None # the CPU architecture
    processor = None # the CPU type

    hostname = None # the name of the host on which this process is running
    platform = None # the OS type on which this process is running


    @property
    def nickname(self, hostname=None):
        """
        Attempt to retrieve the user's assigned nickname for a {host}
        """
        # use my hostname if no host was given
        hostname = self.hostname if hostname is None else hostname
        # get the configuration slots
        slots = [ slot for _,slot in self.pyre_executive.configurator.children(self.hostmapkey) ]
        # go through each one in priority order
        for slot in sorted(slots, key=operator.attrgetter('priority')):
            # get the recognizer
            regex = slot.value
            # if my hostname matches
            if re.match(regex, hostname):
                # return the slot local name as the nickname
                return slot.localname
        # not known; return the original
        return hostname


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior
        """
        # {Executive} is abstract
        raise NotImplementedError("class {.__name__} must implement 'launch'".format(type(self)))


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # host discovery
        (system, name, release, version, architecture, processor) = platform.uname()
        self.hostname = name
        self.system = system
        self.release = release
        self.version = version
        self.architecture = architecture
        self.processor = processor
        self.platform = sys.platform

        # all done
        return


# end of file 
