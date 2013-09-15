# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import re
import merlin
import pyre.tracking


# declaration
class Spellbook(merlin.component, family="merlin.components.spellbook"):
    """
    This is a sample documentation string for Spellbook
    """


    # exceptions
    from .exceptions import SpellNotFoundError


    # types
    from .Spell import Spell as spell


    # public data
    recognizer = re.compile(
        r'^.+\.py$'
        )


    # utilities
    def findSpell(self, name, locator=None):
        """
        Look through the registered spell locations for a spell shelf that contains the given
        spell {name}.
        """
        # print(" ** Spellbook.findSpell: looking for {!r}".format(name))
        # make a locator
        here = pyre.tracking.simple('while looking for spell {!r}'.format(name))
        # and chain it to the locator that was passed in
        locator = pyre.tracking.chain(this=here, next=locator) if locator else here
        # ask the spell interface to convert the name into plausible spell factories
        factory = self.spell().coerce(value=name, locator=locator)
        # place the spell name in the merlin namespace and alias its traits at global scope
        spell = factory(name='merlin.'+name, globalAliases=True)
        # print("    found: {}".format(spell))
        # return the spell instance
        return spell


    def shelves(self, name, folder):
        """
        Iterate over the contents of {folder} and return candidate shelves
        """
        # go through the entire contents
        for shelf in folder.contents:
            # skip unrecognizable files
            if not self.recognizer.match(shelf): continue
            # everybody else is a candidate, for now
            yield folder.join(name, shelf)
        # all done
        return


# end of file
