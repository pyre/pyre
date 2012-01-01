# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import re
import merlin


# declaration
class Spellbook(merlin.component, family="merlin.spells"):
    """
    This is a sample documentation string for Spellbook
    """


    # exceptions
    from .exceptions import SpellNotFoundError


    # public data
    recognizer = re.compile(
        r'^.+\.py$'
        )


    # utilities
    def findSpell(self, name):
        """
        Look through the registered spell locations for a spell shelf that contains the given
        spell {name}.
        """
        # print(" ** Spellbook.findSpell: looking for {!r}".format(name))
        # access to the pyre executive
        executive = self.pyre_executive
        # ask the executive to locate the spell factory
        factory = executive.retrieveComponentDescriptor(uri=name, context=self)
        # place the name in the merlin namespace
        name = 'merlin.' + name
        # instantiate it and alias its traits at global scope
        spell = factory(name=name, globalAliases=True)
        # print("    found: {}".format(spell))
        # and return it
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
