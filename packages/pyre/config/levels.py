# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# priority levels for the various configuration sources
DEFAULT_CONFIGURATION = -1 # defaults from the component declarations
BOOT_CONFIGURATION = 0 # configuration from the standard pyre boot files
PACKAGE_CONFIGURATION = 5 # configuration from package files
USER_CONFIGURATION = 10 # configurations supplied by the end user
EXPLICIT_CONFIGURATION = 15 # programmatic overrides


# end of file 
