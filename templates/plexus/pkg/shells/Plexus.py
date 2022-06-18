# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# externals
import textwrap
# access the pyre framework
import pyre
# and my package
import {project.name}


# declaration
class Plexus(pyre.plexus, family='{project.name}.shells.plexus'):
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
        # the project header
        yield from textwrap.dedent({project.name}.meta.banner).splitlines()
        # the doc string
        yield from self.pyre_showSummary(indent='')
        # the authors
        yield from textwrap.dedent({project.name}.meta.authors).splitlines()
        # all done
        return


    # interactive session management
    def pyre_interactiveSessionContext(self, context=None):
        """
        Go interactive
        """
        # prime the execution context
        context = context or {{}}
        # grant access to my package
        context['{project.name}'] = {project.name}  # my package
        # and chain up
        return super().pyre_interactiveSessionContext(context=context)


# end of file
