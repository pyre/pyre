# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import merlin


# declaration
class Copyright(merlin.spell):
    """
    Print out the merlin copyright note
    """


    # class interface
    # interface
    @merlin.export
    def main(self, **kwds):
        """
        Print the copyright note of the merlin package
        """
        # invoke the package function
        merlin.copyright()
        # all done
        return


    @merlin.export
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """
        # all done
        return


# end of file 
