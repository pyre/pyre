# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import pyre
# superclass
from .Command import Command


# class declaration
class Panel(Command):
    """
    A command that interprets its secondary arguments as method names and invokes them
    """


    # interface
    @pyre.export
    def main(self, plexus, argv):
        """
        Dispatch to my methods based on the names in {argv}
        """
        # realize the argument sequence
        argv = tuple(argv)
        # if there was no command, show the user my help screen
        if not argv: return self.help(plexus=plexus)
        # otherwise, go through my secondary arguments
        for command in argv:
            # attempt to
            try:
                # look each one up
                method = getattr(self, command)
            # if there was a typo
            except AttributeError:
                # show an error message
                self.error.log('{.pyre_spec}: unrecognized command {!r}'.format(self, command))
                # and my help screen
                return self.help(plexus=plexus)
            # otherwise, all is well; attempt to
            try:
                # execute the command
                method(plexus=plexus)
            # if anything goes wrong
            except Exception as error:
                # if we are in debug mode, just let the exception go through
                if plexus.DEBUG: raise
                # otherwise, grab the type of error
                category = type(error).__name__
                # and generate an error message for the user
                self.error.log('{}: {}: {}'.format(command, category, error))
                # and bail
                return 1

        # all done
        return 0


# end of file
