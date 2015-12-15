# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# declaration
class Dashboard:
    """
    Mix-in class that provides access to the pyre executive and its managers
    """

    # grab the base of all pyre exceptions
    from .exceptions import PyreError


    # public data
    # the executive
    pyre_executive = None

    # framework parts
    pyre_fileserver = None
    pyre_nameserver = None
    pyre_configurator = None

    # infrastructure managers
    pyre_registrar = None # the component registrar
    pyre_externals = None # the manager of external packages
    pyre_schema = None # the database schema

    # information about the runtime environment
    pyre_host = None # the current host
    pyre_user = None # the current user


# end of file
