# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import merlin


# declaration
class License(merlin.spell):
    """
    Print out the license and terms of use of the merlin package
    """


    # class interface
    @merlin.export
    def main(self, *args, **kwds):
        """
        Print out the license and terms of use of the merlin package
        """
        # invoke the package function
        merlin.license()
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
