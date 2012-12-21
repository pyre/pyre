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
# the protocols of my traits
from ..platforms import platform


# declaration
class Executive(pyre.component, family='pyre.shells.executive', implements=shell):
    """
    The base class for hosting strategies
    """


    # user configurable state
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"

    host = platform()
    host.doc = "information about the host machine"


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


# end of file 
