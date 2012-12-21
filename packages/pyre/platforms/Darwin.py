# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os
# superclass
from .Host import Host


# declaration
class Darwin(Host, family='pyre.platforms.darwin'):
    """
    Encapsulation of a generic darwin host
    """


    # public data
    platform = 'darwin'
    systemdirs = ['/usr'] # canonical package installation locations


    # protocol obligations
    @classmethod
    def flavor(cls):
        """
        Return a suitable default encapsulation of the runtime host
        """
        # if the macports directory exists
        if os.path.isdir('/opt/local/var/macports'):
            # load the class record
            from .MacPorts import MacPorts
            # and return it
            return MacPorts

        # otherwise, act like a generic darwin system
        return cls


    # implementation details: explorers
    @classmethod
    def cpuServey(cls):
        """
        Collect information about the CPU resources on this host
        """
        # on darwin, we get this information from an extension
        from pyre.extensions import host
        # easy enough
        return host.physicalMax(), host.logicalMax()


# end of file 
