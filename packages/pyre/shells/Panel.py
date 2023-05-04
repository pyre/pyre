# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#


# access to the framework
import pyre
# and the journal
import journal
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
        # if there was no command
        if not argv:
            # attempt to
            try:
                # look for a default action
                default = getattr(self, 'default')
            # if not there
            except AttributeError:
                # show the user my help screen
                return self.help(plexus=plexus)
            # if we have one, invoke it
            return default(plexus=plexus, argv=argv)

        # otherwise, go through my secondary arguments
        for command in argv:
            # attempt to
            try:
                # look each one up
                method = getattr(self, command)
            # if there was a typo
            except AttributeError:
                # show an error message
                plexus.error.log(f"{self.pyre_spec}: unrecognized command '{command}'")
                # and my help screen
                return self.help(plexus=plexus)
            # otherwise, all is well; attempt to
            try:
                # execute the command; hand it a reference to me, so that it has access to the
                # application context, and the argument vector, in case it has opinions about
                # how to interpret the unprocessed command line
                status = method(plexus=plexus, argv=argv)
                # N.B.: there is no need to translate {None} into a numeric value at this
                # point; properly constructed {pyre} harnesses return control to the shell by
                # raising {SystemExit}, which performs this translation

            # if a journal related exception is raised
            except journal.exceptions.JournalError:
                # unless explicitly suppressed, this has been reported already; in either case,
                # leave it alone and just indicate a failure
                return 2
            # if anything else goes wrong
            except Exception as error:
                # if we are in debug mode
                if plexus.DEBUG:
                    # just let the exception go through
                    raise
                # otherwise, grab the type of error
                category = type(error).__name__
                # and generate an error message for the user
                plexus.error.line(f"while executing '{self.pyre_spec} {command}':")
                plexus.error.log(f"    {category}: {error}")
                # and bail
                return 1

        # all done
        return status


# end of file
