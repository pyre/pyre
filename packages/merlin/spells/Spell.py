# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre
from ..components import spell


class Spell(pyre.component, implements=spell):
    """
    Interface declaration for merlin spells
    """


    # public state
    dry = pyre.properties.bool(default=False)
    dry.doc = 'show what would be done without actually doing anything'


    # access to the merlin executive
    merlin = None # patched by the merlin boot sequence


    @property
    def vfs(self):
        """
        Access to my file server
        """
        return self.merlin.vfs


    # interface
    @pyre.export
    def main(self, **kwds):
        """
        This is the action of the spell
        """
        print(" ** casting {!r}".format(self.pyre_name))
        # all done
        return


    @pyre.export
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """
        print(" ** help for {!r}".format(self.pyre_name))
        # all done
        return


# end of file 
