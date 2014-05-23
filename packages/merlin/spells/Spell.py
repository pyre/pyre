# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# framework access
import pyre
# my protocol
from ..components import spell
# access to the merlin singletons
from ..components import dashboard


# class declaration
class Spell(dashboard, pyre.command, implements=spell):
    """
    Interface declaration for merlin spells
    """


    # public state
    dry = pyre.properties.bool(default=False)
    dry.doc = 'show what would be done without actually doing anything'

    # public data
    @property
    def vfs(self):
        """
        Access to the fileserver
        """
        # merlin knows
        return self.merlin.vfs


# end of file 
