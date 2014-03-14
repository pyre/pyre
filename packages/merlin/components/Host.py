# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import merlin
import platform


# declaration
class Host(merlin.component):
    """
    Encapsulation of host specific information
    """


    # public data
    # defaults from the current environment
    (system, name, release, version, architecture, processor) = platform.uname()


# end of file 
