# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import weakref


# declaration
class Client:
    """
    Mix-in class that provides access to the pyre executive and its managers
    """


    # public data
    # the executive
    pyre_executive = None 

    # framework parts
    pyre_registrar = None
    pyre_fileserver = None
    pyre_nameserver = None
    pyre_configurator = None
    pyre_externals = None

    # information about the runtime environment
    pyre_host = None
    pyre_user = None


# end of file 
