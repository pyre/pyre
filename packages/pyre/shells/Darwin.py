# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Platform import Platform


# declaration
class Darwin(Platform, family='pyre.hosts.darwin'):
    """
    Encapsulation of a generic darwin host
    """


    # public data
    platform = 'darwin'


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
