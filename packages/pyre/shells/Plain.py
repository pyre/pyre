# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import collections
# access the framework
import pyre
# get my protocol
from .Terminal import Terminal as terminal


# declaration
class Plain(pyre.component, family='pyre.shells.terminals.plain', implements=terminal):


    # implementation details
    colors = collections.defaultdict(str) # all color decorations are empty strings...


# end of file
