# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# declaration
class Dashboard:
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
