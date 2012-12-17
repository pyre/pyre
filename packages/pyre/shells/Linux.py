# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Platform import Platform


# declaration
class Linux(Platform, family='pyre.hosts.linux'):
    """
    Encapsulation of a generic linux host
    """


    # public data
    platform = 'linux'


# end of file 
