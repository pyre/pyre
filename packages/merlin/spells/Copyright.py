# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    def main(self, plexus, argv):
        """
        Print the copyright note of the merlin package
        """
        # invoke the package function
        merlin.copyright()
        # all done
        return


# end of file
