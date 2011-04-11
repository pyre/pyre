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
class License(Spell):
    """
    Print out the license and terms of use of the merlin package
    """


    # class interface
    # interface
    @pyre.export
    def main(self, **kwds):
        """
        Print out the license and terms of use of the merlin package
        """
        # access to the merlin package
        import merlin
        # invoke the package function
        merlin.license()
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
