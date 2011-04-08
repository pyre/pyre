# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# superclasses
from .Spell import Spell


# declaration
class Initializer(Spell):
    """
    This is a sample documentation string for class Initializer
    """


    # class interface
    # interface
    @pyre.export
    def main(self, **kwds):
        """
        This is the action of the spell
        """
        print(" ** new project here")
        # all done
        return


    @pyre.export
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """
        # all done
        return


# end of file 
