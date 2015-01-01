# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    def main(self, plexus, argv):
        """
        Print the version of the merlin package
        """
        # invoke the package function
        print(merlin._merlin_header)
        # all done
        return


# end of file
