# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Darwin import Darwin


# declaration
class MacPorts(Darwin, family='pyre.platforms.macports'):
    """
    Encapsulation of a darwin host that runs macports
    """

    # public data
    systemdirs = ['/opt/local'] + Darwin.systemdirs # canonical package installation locations


# end of file 
