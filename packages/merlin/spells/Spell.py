# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..components import spell


class Spell(pyre.component, implements=spell):
    """
    Interface declaration for merlin spells
    """


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
