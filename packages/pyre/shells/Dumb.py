# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import collections
# access the framework
import pyre
# get my protocol
from .Terminal import Terminal as terminal


# declaration
class Dumb(pyre.component, family='pyre.terminals.dumb', implements=terminal):


    # implementation details
    colors = collections.defaultdict(str)


# end of file 
