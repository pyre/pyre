# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# access to the framework
import pyre

# superclass
from .Application import Application

# my parts
from .Repertoire import Repertoire


# class declaration
class Plexus(Application):
    """
    Base class for applications that interpret their first non-configurational command line
    argument as an action that should be executed.

    As an example of such an app, consider {merlin}. Invoking

        merlin info

    causes the {merlin} plexus to locate an action named {info} and invoke it.

    Subclasses are expected to declare a class variable {pyre_action} that points to a subclass
    of the {Action} protocol defined in this package. This responsibility is left to subclasses
    so that there is no bias on the category names of the actions induced by a choice of family
    name by the framework. This way the language used to specify the actions and their behavior
    can remain natural to the context of the application.
    """

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The plexus main entry point interprets the first non-configurational command line argument
        as the name of an action to perform
        """
        # grab my command line arguments
        argv = tuple(self.argv)
        # if there is nothing to invoke
        if not argv:
            # just show the help screen
            return self.help()
        # otherwise, interpret the first argument as a command and invoke it
        return self.pyre_invoke(action=argv[0], argv=argv[1:])

    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        # grab my command line arguments
        argv = self.argv
        # and attempt to
        try:
            # get the name of a command
            name = next(argv)
        # if there wasn't one
        except StopIteration:
            # no worries, we handle this case below
            pass
        # if there was one
        else:
            # we have the name of a command; resolve it
            command = self.pyre_repertoire.resolve(plexus=self, spec=name)
            # and invoke its help
            return command.help(plexus=self)

        # if we get this far, the user has asked for help without specifying a particular
        # command; display the general help screen
        return super().help(**kwds)

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my repertoire
        self.pyre_repertoire = self.pyre_newRepertoire()
        # all done
        return

    # implementation details
    # hooks
    def pyre_newRepertoire(self):
        """
        Factory for the manager of actions
        """
        # build one using the default implementation and return it
        return Repertoire(protocol=self.pyre_action)

    # convenience
    def pyre_actions(self):
        """
        Retrieve all known implementations of my action
        """
        # initialize my cache
        actions = {}
        # ask my action specification for help
        for uri, name, action, tip in self.pyre_action.pyre_actions(plexus=self):
            # if i already know this one
            if name in actions:
                # move on
                continue
            # otherwise, add it to the pile
            actions[name] = (uri, action, tip)
            # and make it available
            yield uri, name, action, tip
        # all done
        return

    def pyre_documentedActions(self):
        """
        Retrieve all public implementations of my action
        """
        # go through all the actions
        for uri, name, action, tip in self.pyre_actions():
            # undocumented ones
            if tip is None:
                # get skipped
                continue
            # everything else is good
            yield uri, name, action, tip
        # all done
        return

    def pyre_invoke(self, action, argv=None):
        """
        Invoke the named {action} with {argv} as additional arguments
        """
        # make sure {argv} is iterable
        argv = [] if argv is None else argv
        # resolve and invoke; typos and such get handled by {pyre_repertoire}
        return self.pyre_repertoire.invoke(plexus=self, action=action, argv=argv)

    # support for the help system
    def pyre_help(self, indent=" " * 2, **kwds):
        """
        Hook for the plexus help system
        """
        # the application banner
        yield from self.pyre_banner()
        # the available actions
        yield from self.pyre_documentActions(indent=indent)
        # the configurable state
        yield from self.pyre_showConfigurables(indent=indent)
        # all done
        return

    def pyre_documentActions(self, indent=" " * 2):
        """
        Place information about the available actions in my {info} channel
        """
        # initialize the pile of known actions
        actions = []
        # get the documented commands
        for _, name, _, tip in self.pyre_action.pyre_documentedActions(plexus=self):
            # and put them on the pile
            actions.append((name, tip))
        # if there were any
        if actions:
            # figure out how much space we need
            width = max(len(name) for name, _ in actions)
            # introduce this section
            yield ""
            yield "commands:"
            # for each documented action
            for name, tip in actions:
                # show the details
                yield f"{indent}{name:>{width}}: {tip}"
            # add some space
            yield ""

        # all done
        return

    # data
    pyre_repertoire = None


# end of file
