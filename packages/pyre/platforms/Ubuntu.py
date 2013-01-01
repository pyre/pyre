# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import re
# superclass
from .Linux import Linux


# declaration
class Ubuntu(Linux, family='pyre.platforms.ubuntu'):
    """
    Encapsulation of a host running linux on the ubuntu distribution
    """


    # public data
    distribution = 'ubuntu'


# end of file 
