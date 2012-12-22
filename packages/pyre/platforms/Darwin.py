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
    distribution = 'apple'
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


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # use to set the codename
        self.release, self.codename = self.getDarwinInfo()
        # all done
        return


    # implementation details: explorers
    @classmethod
    def cpuSurvey(cls):
        """
        Collect information about the CPU resources on this host
        """
        # on darwin, we get this information from an extension
        from pyre.extensions import host
        # easy enough
        return host.physicalMax(), host.logicalMax()


    @classmethod
    def getDarwinInfo(cls):
        # ask the platform package
        import platform
        # for the release number
        release, _, _ = platform.mac_ver()
        # extract {major.minor}
        marker, _ = release.rsplit('.', 1)
        # use the marker to get the codename
        codename = cls.codenames.get(marker, 'unknown')
        # and return
        return release, codename


    # private data
    # the known code names
    codenames = {
        '10.8': 'mountain lion',
        '10.7': 'lion',
        '10.6': 'snow leopard',
        '10.5': 'leopard',
        '10.4': 'tiger',
        '10.3': 'panther',
        '10.2': 'jaguar',
        '10.1': 'puma',
        '10.0': 'cheetah',
        }

# end of file 
