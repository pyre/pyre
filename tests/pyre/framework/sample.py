# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

import pyre

def factory(): pass

class base(pyre.component):
    """A trivial component"""

class d1(base):
    """A trivial component subclass"""

class d2(base):
    """A trivial component subclass"""

# end of file 
