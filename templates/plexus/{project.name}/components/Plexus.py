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
        # set the indentation
        indent = ' '*4
        # make some space
        self.info.line()
        # get the help header
        for line in {project.name}._{project.name}_header.splitlines():
            # and display it
            self.info.line(line)

        # reset the pile of actions
        actions = []
        # get the documented commands
        for uri, name, action, tip in self.pyre_action.pyre_documentedActions():
            # and put them on the pile
            actions.append((name, tip))
        # if there were any
        if actions:
            # figure out how much space we need
            width = max(len(name) for name, _ in actions)
            # introduce this section
            self.info.line('commands:')
            # for each documented action
            for name, tip in actions:
                # show the details
                self.info.line('{{}}{{:>{{}}}}: {{}}'.format(indent, name, width, tip))
            # some space
            self.info.line()

        # flush
        self.info.log()
        # and indicate success
        return 0


# end of file
