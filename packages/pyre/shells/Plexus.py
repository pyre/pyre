# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import pyre
# superclass
from .Application import Application


# class declaration
class Plexus(Application):
    """
    Base class for applications that interpret their first non-configurational command line
    argument as an action that should be executed.

    As an example of such an app, consider {merlin}. Invoking

        merlin version

    causes the {merlin} plexus to locate an action named {version} and invoke it.

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
        argv = self.argv
        # attempt to
        try:
            # get the name of the command
            name = next(argv)
        # if there aren't any
        except StopIteration:
            # if the user has requested an interactive session
            if self.interactive:
                # do it
                return self.pyre_interactiveSession()
            # otherwise, show the help screen
            return self.help()

        # invoke the command
        return self.repertoir.invoke(plexus=self, action=name, argv=argv)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my repertoir
        self.repertoir = self.newRepertoir()
        # all done
        return


    # implementation details
    # hooks
    def newRepertoir(self):
        """
        Factory for the manager of actions
        """
        # get the default implementation
        from .Repertoir import Repertoir
        # build one and return it
        return Repertoir(protocol=self.pyre_action)


    # data
    repertoir = None


# end of file
