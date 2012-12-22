# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import re
# superclass
from .Linux import Linux


# declaration
class RedHat(Linux, family='pyre.platforms.redhat'):
    """
    Encapsulation of a host running linux on the ubuntu distribution
    """


    # public data
    distribution = 'redhat'


# end of file 
