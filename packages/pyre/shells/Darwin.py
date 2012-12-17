# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Platform import Platform


# declaration
class Darwin(Platform, family='pyre.hosts.darwin'):
    """
    Encapsulation of a generic darwin host
    """


    # public data
    platform = 'darwin'


# end of file 
