# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    def main(self, plexus, argv):
        """
        Print out the license and terms of use of the merlin package
        """
        # invoke the package function
        merlin.license()
        # all done
        return


# end of file
