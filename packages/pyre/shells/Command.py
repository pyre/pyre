# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# access to the framework
import pyre
import journal
# my protocol
from .Action import Action


# class declaration
class Command(pyre.component, implements=Action):
    """
    A component that implements {Action}
    """


    # public state
    dry = pyre.properties.bool(default=False)
    dry.doc = "show what would get done without actually doing anything"


    # expected interface
    @pyre.export
    def main(self, plexus, **kwds):
        """
        This is the implementation of the action
        """
        # just print a message
        plexus.info.log('main: missing implementation')
        # and indicate success
        return 0


    @pyre.export(tip='show this help screen')
    def help(self, plexus, **kwds):
        """
        Show a help screen
        """
        # make a channel
        channel = journal.help("pyre.help.command")
        # build my help screen
        channel.report(report=self.pyre_help(plexus=plexus))
        # and flush
        channel.log()
        # all done
        return 0


    # meta-methods
    def __init__(self, name, spec, plexus, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # save my short name
        self.pyre_spec = spec
        # all done
        return


    # implementation details
    def __call__(self, plexus, argv):
        """
        Commands are callable
        """
        # delegate to {main}
        return self.main(plexus=plexus, argv=argv)


    def pyre_help(self, plexus, indent=' '*2, **kwds):
        """
        Hook for the application help system
        """
        # build my specification
        spec = f"{plexus.pyre_namespace} {self.pyre_spec}"
        # and render it
        yield spec

        # my summary
        yield from self.pyre_showSummary(indent=indent, **kwds)
        # my behaviors
        yield from self.pyre_showBehaviors(spec=spec, indent=indent, **kwds)
        # my public state
        yield from self.pyre_showConfigurables(indent=indent, **kwds)
        # all done
        return


    # private data
    pyre_spec = None


# end of file
