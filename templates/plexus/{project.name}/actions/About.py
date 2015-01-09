# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# externals
import {project.name}


# declaration
class About({project.name}.command, family='{project.name}.actions.about'):
    """
    Display information about this application
    """


    # user configurable state
    prefix = {project.name}.properties.str()
    prefix.tip = "specify the portion of the namespace to display"


    # class interface
    @{project.name}.export(tip="print the copyright note")
    def copyright(self, plexus):
        """
        Print the copyright note of the {project.name} package
        """
        # get the lines
        for line in {project.name}._{project.name}_copyright.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @{project.name}.export(tip="print out the acknowledgments")
    def credits(self, plexus):
        """
        Print out the license and terms of use of the {project.name} package
        """
        # make some space
        plexus.info.line()
        # get the lines
        for line in {project.name}._{project.name}_acknowledgments.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @{project.name}.export(tip="print out the license and terms of use")
    def license(self, plexus):
        """
        Print out the license and terms of use of the {project.name} package
        """
        # make some space
        plexus.info.line()
        # get the lines
        for line in {project.name}._{project.name}_license.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @{project.name}.export(tip='dump the application configuration namespace')
    def nfs(self, plexus):
        """
        Dump the application configuration namespace
        """
        # get the prefix
        prefix = self.prefix or '{project.name}'
        # show me
        plexus.pyre_nameserver.dump(prefix)
        # all done
        return


    @{project.name}.export(tip="print the version number")
    def version(self, plexus):
        """
        Print the version of the {project.name} package
        """
        # make some space
        plexus.info.line()
        # invoke the package header and push it to the plexus info channel
        plexus.info.log({project.name}._{project.name}_header)
        # all done
        return


    @{project.name}.export(tip='dump the application virtual filesystem')
    def vfs(self, plexus):
        """
        Dump the application virtual filesystem
        """
        # get the prefix
        prefix = self.prefix or '/{project.name}'
        # show me
        plexus.vfs[prefix].dump()
        # all done
        return


# end of file
