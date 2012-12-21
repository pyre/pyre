# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# the protocol
from .Platform import Platform as platform

# the various implementations
# darwin
from .Darwin import Darwin as darwin
from .MacPorts import MacPorts as macports
# linux
from .Linux import Linux as linux
from .CentOS import CentOS as centos
from .RedHat import RedHat as redhat
from .Ubuntu import Ubuntu as ubuntu


# end of file 
