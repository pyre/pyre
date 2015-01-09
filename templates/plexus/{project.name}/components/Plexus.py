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
class Plexus(pyre.plexus, family='{project.name}.components.plexus'):
    """
    The main action dispatcher
    """


    # constants
    pyre_namespace = '{project.name}'
    # types
    from .Action import Action as pyre_action


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


# end of file
