# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access the framework
import pyre
# and the merlin singletons
from .Dashboard import Dashboard as dashboard


# declaration
class Spell(pyre.action, dashboard, family="merlin.spells"):
    """
    Protocol declaration for merlin spells
    """


    # support for framework requests
    @classmethod
    def pyre_contextPath(cls):
        """
        Return an iterable over the starting point for hunting down spells
        """
        # merlin knows
        return cls.merlin.searchpath


    @classmethod
    def pyre_contextFolders(cls):
        """
        Return an iterable over portions of my family name
        """
        # spells are in the 'spells' folder
        return [ 'spells' ]



# end of file
