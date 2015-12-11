# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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

        # get the macports package manager
        from .MacPorts import MacPorts as macports
        # if this is a macports system
        if macports.prefix():
            # return it as the flavor
            return macports

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
            return super().cpuSurvey()
        # otherwise, return the information given by OSX
        return host.physicalMax(), host.logicalMax()


    @classmethod
    def getOSInfo(cls):
        # ask the platform package
        import platform
        # for the release number
        release, _, _ = platform.mac_ver()
        # extract the major release
        major = '.'.join(release.split('.')[:2])
        # use it to get the codename
        codename = cls.codenames.get(major, 'unknown')
        # and return
        return release, codename


    # private data
    # the known code names
    codenames = {
        '10.11': 'el capitan',
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
