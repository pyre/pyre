# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import collections
# access the framework
import pyre
# get my protocol
from .Terminal import Terminal as terminal


# declaration
class Plain(pyre.component, family='pyre.terminals.plain', implements=terminal):
    """
    A terminal that provides no color capabilities
    """

    # interface
    def rgb(self, **kwds):
        """
        The 24-bit color request
        """
        # we don't do that...
        return''


    def rgb256(self, rgb, foreground=True):
        """
        The 256-color palette request
        """
        # we don't do that either...
        return''


    # implementation details
    colors = collections.defaultdict(str) # all color decorations are empty strings...


# end of file
