# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os
# superclass
from .POSIX import POSIX


# declaration
class Darwin(POSIX, family='pyre.platforms.darwin'):
    """
    Encapsulation of a generic darwin host
    """


    # public data
    platform = 'darwin'
    distribution = 'apple'


    # protocol obligations
    @classmethod
    def flavor(cls):
        """
        Return a suitable default encapsulation of the runtime host
        """
        # set the release and the codename
        cls.release, cls.codename = cls.getOSInfo()

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
    def cpuSurvey(cls):
        """
        Collect information about the CPU resources on this host
        """
        # on darwin, we get this information from an extension
        try:
            # we get this information from an extension
            from pyre.extensions import host
        # which may not be accessible, e.g. if pyre is executed from within a zipfile
        except ImportError:
            # revert to defaults
            return 1,1
        # otherwise, return the information given by OSX
        return host.physicalMax(), host.logicalMax()


    @classmethod
    def getOSInfo(cls):
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
        '10.10': 'yosemite',
        '10.9': 'mavericks',
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
