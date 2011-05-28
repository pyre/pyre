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

    # constants
    context = ["merlin", "spells"]


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
        factory = executive.retrieveComponentDescriptor(uri=name, context=self.context)
        # instantiate it
        spell = factory(name=name)
        # and return it
        return spell


    def volumes(self):
        """
        Iterate over all the spell files in all the standard places
        """
        # access the file server
        vfs = self.pyre_executive.fileserver
        # iterate over the standard locations
        for archive in self.archives:
            # ask the file server for the matching folder
            try:
                folder = vfs[archive]
            # if not there, move on...
            except vfs.NotFoundError:
                continue
            # now, iterate over the contents of the folder
            for volume in folder.contents:
                # form the name of the volume
               yield folder.join(archive, volume)
        # all done
        return
                

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
