# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# the framework
import pyre
# externals
import re
import operator


# declaration
class Host(pyre.protocol, family='pyre.hosts'):
    """
    Encapsulation of host specific information
    """


    # constants
    # the key under which users specify nicknames for known hosts
    hostmapkey = 'pyre\.hostmap\..+'


    # framework obligations
    @classmethod
    def pyre_default(cls):
        """
        Build the preferred host implementation
        """
        # get the nameserver
        nameserver = cls.pyre_nameserver
        # get the host name
        import platform
        hostname = platform.node()

        # look for the entries under the {hostmap} key
        hosts = nameserver.find(pattern=cls.hostmapkey)
        # go through them in priority order
        for name, slot in sorted(hosts, key=lambda x: x[1].priority):
            # get the regular expression from the slot value
            regex = slot.value
            # if my hostname matches 
            if re.match(regex, hostname):
                # extract the nickname as the last part of the key name
                nickname = nameserver.split(name)[-1]
                # return a component specification for this nickname
                return "{}".format(nickname)
        
        # get the platform id
        import sys
        platform = sys.platform

        # if we are on darwin
        if platform.startswith('darwin'):
            # get the {Darwin} host wrapper
            from .Darwin import Darwin
            # and ask it for a suitable default implementation
            return Darwin.flavor()

        # if we are on a linux derivative
        if platform.startswith('linux'):
            # get the {Linux} host wrapper
            from .Linux import Linux
            # and ask it for a suitable default implementation
            return Linux.flavor()

        # otherwise, we know nothing; let the user know
        from .Platform import Platform
        return Platform


# end of file 
