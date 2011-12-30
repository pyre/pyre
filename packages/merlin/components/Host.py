# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import platform


# declaration
class Host(pyre.component):
    """
    Encapsulation of host specific information
    """


    # public data
    # defaults from the current environment
    (system, name, release, version, processor, architecture) = platform.uname()


# end of file 
