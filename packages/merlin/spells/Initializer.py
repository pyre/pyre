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
class Initializer(Spell):
    """
    Create a new merlin project rooted at the given directory
    """


    # public state
    createPrefix = pyre.properties.bool(default=False)
    createPrefix.aliases.add('create-prefix')


    # class interface
    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        Make {folder} the root of a new merlin project. The target {folder} is given as an
        optional command line argument, and defaults to the current directory. Issue an error
        message if {folder} is already a merlin project.
        """
        # NYI: non-local uris
        print('name:', self.pyre_name)
        # access my executive
        merlin = self.merlin

        # the first argument is supposed to be a subdirectory of the current directory
        folder = args[0] if args else os.curdir
        print("target folder: {!r}".format(folder))

        # first check whether this directory is already part of a merlin project
        root, metadir = merlin.locateProjectRoot(folder=folder)
        # if it is
        if root:
            # complain
            import journal
            msg = "{!r} is already within an existing project".format(folder)
            return journal.error("merlin.init").log(msg)

        return

        # otherwise, if the directory does not exist
        if not os.path.isdir(folder):
            print("  does not exist; creating")
            # were we asked to build all parent directories?
            if self.createPrefix:
                # yes, do it
                print("    including all intermediates")
                # os.makedirs(os.path.abspath(folder))

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
