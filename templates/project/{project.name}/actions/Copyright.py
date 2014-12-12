# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# externals
import {project.name}


# declaration
class Copyright({project.name}.command, family='{project.name}.actions.copyright'):
    """
    Print out the {project.name} copyright note
    """


    # class interface
    # interface
    @{project.name}.export
    def main(self, plexus, argv):
        """
        Print the copyright note of the {project.name} package
        """
        # invoke the package function
        print({project.name}.copyright())
        # all done
        return


# end of file
