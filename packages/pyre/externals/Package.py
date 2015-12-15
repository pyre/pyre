# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access the pyre framework
import pyre


# protocol declaration
class Package(pyre.protocol, family='pyre.externals'):
    """
    The protocol that all external package managers must implement
    """


    # configurable state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    # constants
    category = None # the common name for this package category

    # exceptions
    from pyre.framework.exceptions import ExternalNotFoundError


# end of file
