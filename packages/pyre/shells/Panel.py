# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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

    # constants
    SUCCESS = 0
    ERROR_GENERIC = 1
    ERROR_EXECUTION = 2
    ERROR_UNRECOGNIZED_COMMAND = 3

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
                default = getattr(self, "default")
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
            # if there was some kind of typo
            except AttributeError:
                # handle the error
                return self.pyre_unrecognizedCommand(
                    plexus=plexus, command=command, argv=argv
                )

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
                return self.ERROR_GENERIC

            # if anything else goes wrong
            except Exception as error:
                # if we are in debug mode
                if plexus.DEBUG:
                    # just let the exception go through
                    raise
                # otherwise, grab the type of error
                category = type(error).__name__
                # get a channel
                channel = plexus.error
                # generate an error message for the user
                channel.line(f"{category}: {error}")
                channel.line(f"while executing '{self.pyre_spec} {command}':")
                # flush
                channel.log()
                # and bail
                return self.ERROR_EXECUTION

        # all done
        return status

    # failure modes
    def pyre_unrecognizedCommand(self, plexus, command, **kwds):
        """
        Handler invoked when the {panel} does not recognize a command
        """
        # show an error message
        plexus.error.log(f"{self.pyre_spec}: unrecognized command '{command}'")
        # and my help screen
        return self.help(plexus=plexus)
        # indicate failure
        return self.ERROR_UNRECOGNIZED_COMMAND


# end of file
