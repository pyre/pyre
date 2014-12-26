# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# access the pyre framework
import pyre
# my action protocol
from .Action import Action


# declaration
class Plexus(pyre.plexus, family='{project.name}.components.plexus', action=Action):
    """
    The main action dispatcher
    """


    # constants
    pyre_namespace = '{project.name}'


    # plexus obligations
    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        # get the package
        import {project.name}
        # show me
        self.info.log({project.name}._{project.name}_usage)
        # all done
        return 0


    # initialization hooks
    def pyre_mountApplicationFolders(self, pfs, prefix):
        """
        Map the standard runtime folder layout into my private filespace

        Currently, there are two runtime folders that i am interested in:

           {{prefix}}/etc/{{self.pyre_namespace}}: contains application auxiliary data
           {{prefix}}/var/{{self.pyre_namespace}}: contains the application runtime state
        """
        # chain up
        pfs = super().pyre_mountApplicationFolders(pfs=pfs, prefix=prefix)

        # my runtime folders
        folders = [ 'etc', 'var' ]
        # go through them
        for folder in folders:
            # and mount each one
            self.pyre_mountPrivateFolder(pfs=pfs, prefix=prefix, folder=folder)

        # return my {{pfs}}
        return pfs


# end of file
