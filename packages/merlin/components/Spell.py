# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre


class Spell(pyre.interface, familly="merlin.spells"):
    """
    Interface declaration for merlin spells
    """


    # interface
    @pyre.provides
    def main(self, **kwds):
        """
        This is the action of the spell
        """


    @pyre.provides
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """


# end of file 
