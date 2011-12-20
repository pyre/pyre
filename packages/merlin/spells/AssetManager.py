# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import os
import pyre


# superclasses
from .Spell import Spell


# declaration
class AssetManager(Spell):
    """
    Attempt to classify a folder as an asset container and add it to the project
    """


    # class interface
    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        This is the action of the spell
        """
        # the first argument is supposed to be a subdirectory of the current directory
        folder = args[0] if args else '.'
        print('target folder: {!r}'.format(folder))
        # all done
        return


    @pyre.export
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """
        # all done
        return


# end of file 
