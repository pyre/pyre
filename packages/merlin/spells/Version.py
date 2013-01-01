# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import merlin


# declaration
class Version(merlin.spell):
    """
    Print out the version of the merlin package
    """


    # interface
    @merlin.export
    def main(self, *args, **kwds):
        """
        Print the version of the merlin package
        """
        # invoke the package function
        merlin.version()
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
