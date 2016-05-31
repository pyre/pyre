# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# access the pyre framework
import pyre
# and my package
import {project.name}
# my action protocol
from .Action import Action


# declaration
class Plexus(pyre.plexus, family='{project.name}.components.plexus'):
    """
    The main action dispatcher
    """

    # types
    from .Action import Action as pyre_action


    # pyre framework hooks
    # support for the help system
    def pyre_banner(self):
        """
        Generate the help banner
        """
        # show the license header
        return {project.name}.version.license


    # interactive session management
    def pyre_interactiveSessionContext(self, context):
        """
        Go interactive
        """
        # protect against bad contexts
        if context is None:
            # by initializing as an empty dict
            context = {{}}

        # set up some context
        context['{project.name}'] = {project.name}  # my package

        # and chain up
        return super().pyre_interactiveSessionContext(context=context)


# end of file
