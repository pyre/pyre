# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre


# my metaclass
from pyre.patterns.Singleton import Singleton


class Merlin(metaclass=Singleton):
    """
    The merlin executive
    """


    # public data
    executive = pyre.executive # access to the pyre executive


    # interface
    def main(self):
        """
        The main entry point for merlin
        """
        # extract the non-configurational parts of the command line
        request = tuple(c for p,c,l in self.executive.configurator.commands)

        # show the help screen if there was nothing useful on the command line
        if request == (): return self.help()

        # interpret the request as the name of one of my actors, followed by an argument tuple
        # for the actor's main entry point
        componentName = request[0]
        args = request[1:]

        # convert the component name into a uri
        uri = "import://merlin#{}".format(componentName)

        # attempt to retrieve the component factory
        try:
            factory = self.executive.retrieveComponentDescriptor(uri)
        except self.executive.FrameworkError:
            import merlin
            # NYI: try other component sources
            return merlin.usage()

        # instantiate the component
        actor = factory(name="merlin-"+componentName)

        # if it is a merlin actor
        if isinstance(actor, pyre.component):
            # ask it to process the user request
            actor.exec(*args)

        # all done
        return self


# end of file 
