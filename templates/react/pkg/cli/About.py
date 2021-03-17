# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# externals
import {project.name}


# declaration
class About({project.name}.shells.command, family='{project.name}.cli.about'):
    """
    Display information about this application
    """


    @{project.name}.export(tip="print the copyright note")
    def copyright(self, plexus, **kwds):
        """
        Print the copyright note of the {project.name} package
        """
        # show the copyright note
        plexus.info.log({project.name}.meta.copyright)
        # all done
        return


    @{project.name}.export(tip="print out the acknowledgments")
    def credits(self, plexus, **kwds):
        """
        Print out the license and terms of use of the {project.name} package
        """
        # make some space
        plexus.info.log({project.name}.meta.header)
        # all done
        return


    @{project.name}.export(tip="print out the license and terms of use")
    def license(self, plexus, **kwds):
        """
        Print out the license and terms of use of the {project.name} package
        """
        # make some space
        plexus.info.log({project.name}.meta.license)
        # all done
        return


    @{project.name}.export(tip="print the version number")
    def version(self, plexus, **kwds):
        """
        Print the version of the {project.name} package
        """
        # make some space
        plexus.info.log({project.name}.meta.header)
        # all done
        return


# end of file
