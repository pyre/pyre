# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to the framework
import pyre
# superclass
from .Application import Application
# metaclass
from .Plector import Plector


# class declaration
class Plexus(Application, metaclass=Plector):
    """
    Base class for applications that interpret their first non-configurational command line
    argument as an action that should be executed.

    As an example of such an app, consider {merlin}. Invoking

        merlin version

    causes the {merlin} plexus to locate an action named {version} and invoke it.

    Subclasses are expected to declare a trait {action} that implements a subclass of the
    {Action} protocol defined in this package. This responsibility is left to subclasses so
    that there is no bias on the category names of the actions induced by a choice of family
    name by the framework. This way the language used to specify the actions and their behavior
    can remain natural to the context of the application.
    """


    @pyre.export
    def main(self, *args, **kwds):
        """
        The plexus main entry point interprets the first non-configurational command line argument
        as the name of an action to perform
        """
        # grab my command line arguments
        argv = self.argv
        # attempt
        try:
            # to grab the first one and interpret it as an action
            self.pyre_action = next(argv)
        # if there aren't any
        except StopIteration:
            # the user needs help
            return self.help()
        
        # invoke the action
        return self.pyre_action(plexus=self, argv=argv)


# end of file
