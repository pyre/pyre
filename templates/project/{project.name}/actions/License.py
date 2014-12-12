# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# externals
import {project.name}


# declaration
class License({project.name}.command, family='{project.name}.actions.license'):
    """
    Print out the license and terms of use of the {project.name} package
    """


    # class interface
    @{project.name}.export
    def main(self, plexus, argv):
        """
        Print out the license and terms of use of the {project.name} package
        """
        # invoke the package function
        print({project.name}.license())
        # all done
        return


# end of file
