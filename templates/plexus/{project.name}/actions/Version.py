# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import {project.name}


# declaration
class Version({project.name}.command, family='{project.name}.actions.version'):
    """
    Print out the version of the {project.name} package
    """


    # interface
    @{project.name}.export
    def main(self, plexus, argv):
        """
        Print the version of the {project.name} package
        """
        # invoke the package function
        print({project.name}._{project.name}_header)
        # all done
        return


# end of file
