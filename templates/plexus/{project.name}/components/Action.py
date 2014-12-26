# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# access the framework
import pyre


# protocol declaration
class Action(pyre.action, family='{project.name}.actions'):
    """
    Protocol declaration for {project.name} commands
    """


    @classmethod
    def pyre_contextPath(cls):
        """
        Return an iterable over the starting point for hunting down my actions
        """
        # build a string to uri converter
        uri = cls.uri()
        # first mine, then the ones i inherit from pyre
        return [ uri.coerce(value='vfs:/{project.name}'), uri.coerce(value='vfs:/pyre') ]


    @classmethod
    def pyre_contextFolders(cls):
        """
        Return an iterable over portions of my family name
        """
        # actions are in the 'actions' folder
        return [ 'actions' ]


# end of file
