# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre


# declaration
class Spellbook(pyre.component, family="merlin.spellbook"):
    """
    This is a sample documentation string for Spellbook
    """

    # exceptions
    from .exceptions import SpellNotFoundError


    # utilities
    def findSpell(self, name):
        """
        Look through the registered spell locations for a spell shelf that contains the given
        spell {name}.
        """
        # print("Spellbook.findSpell: looking for {!r}".format(name))
        # access to the pyre executive
        executive = self.pyre_executive
        # ask the executive to locate the spell factory
        factory = executive.locateComponentDescriptor(component=name, locations=self.archives)
        # instantiate it
        spell = factory(name=name)
        # and return it
        return spell


    # meta methods
    def __init__(self, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        # the ordered list of locations with spell archives
        self.archives = [
            '/merlin/project/spells',
            '/merlin/user/spells',
            '/merlin/system/spells',
            ]

        return


# end of file 
