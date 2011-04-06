# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import re
# access to the framework
import pyre


# declaration
class Spellbook(pyre.component, family="merlin.spellbook"):
    """
    This is a sample documentation string for Spellbook
    """

    # per instance public data


    # utilities
    def findSpell(self, spell):
        """
        Look through the registered spell locations for a spell shelf that contains the given
        {spell} name.
        """
        print("Spellbook.findSpell: looking for {!r}".format(spell))
        # access to the pyre executive
        executive = self.pyre_executive
        # iterate over the registered archives
        for archive in self.archives:
            print("  looking in {!r}".format(archive))
            # ask the file server for the matching folder
            try:
                folder = executive.fileserver[archive]
            # if not there, move on...
            except executive.fileserver.NotFoundError:
                print("    archive does not exist")
                continue
            # now, iterate over the contents of the folder
            for entry in folder.contents:
                # form the name of the item
                address = folder.join(archive, entry)
                # try to load the associated shelf
                try:
                    shelf = executive._loadShelf(
                        scheme="vfs", authority=None, address=address, locator=None)
                except pyre.PyreError:
                    continue
                # try to look up the spell
                try:
                    factory = shelf.retrieveSymbol(spell)
                except pyre.PyreError:
                    continue
                # instantiate it
                instance = factory(name=spell)
                # and return it
                return instance
        # couldn't find the spell
        raise self.SpellNotFoundError(spell=spell)


    # meta methods
    def __init__(self, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)
        print(" ** spellbook initialization")

        self.archives = [
            '/merlin/project/spells',
            '/merlin/user/spells',
            '/merlin/system/spells',
            ]

        return


# end of file 
