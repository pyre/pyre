# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# externals
import {project.name}


# declaration
class Info({project.name}.command, family='{project.name}.actions.info'):
    """
    Display information about this application
    """


    # user configurable state
    prefix = {project.name}.properties.str()
    prefix.tip = "specify the portion of the namespace to display"


    # class interface
    @{project.name}.export(tip='convenience action for debugging the plexus')
    def test(self, plexus):
        """
        Convenient resting point for debugging code during development
        """
        # show me
        self.info.log('debugging...')
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
