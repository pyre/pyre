# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import tracking
# superclass
from .Executive import Executive


# declaration
class Pyre(Executive):
    """
    The default framework executive.

    This class is responsible for the actual instantiation of the providers of the framework
    services.
    """


    # constants
    locator = tracking.simple('during pyre startup')

    # public data
    from . import _verbose as verbose


    # interface
    def boot(self, **kwds):
        """
        Initialize the providers of the runtime services
        """
        # chain up to my base class
        super().boot(**kwds)

        # local names for my managers
        nameserver = self.nameserver
        configurator = self.configurator

        # access the command line
        import sys
        # make a parser
        parser = self.newCommandLineParser()
        # parse the command line
        events = parser.parse(argv=sys.argv[1:])
        # ask my configurator to process the configuration events
        configurator.processEvents(events=events, priority=self.priority.user)

        # force the loading of the global configuration options
        nameserver.package(executive=self, name="pyre", locator=self.locator)

        # report the boot time errors
        if self.verbose and self.errors:
            print(' ** pyre: the following errors were encountered while booting:')
            for error in self.errors:
                print(' ++   {}'.format(error))

        # all done
        return self


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # my nameserver
        self.nameserver = self.newNameServer()
        # my fileserver
        self.fileserver = self.newFileServer()
        # component bookkeeping
        self.registrar = self.newComponentRegistrar()
        # handler of configuration events
        self.configurator = self.newConfigurator(executive=self)
        # component linker
        self.linker = self.newLinker()
        # the timer registry
        self.timekeeper = self.newTimerRegistry()
        # the manager of external tools and libraries
        self.externals = self.newExternalsManager()

        # critical step: record this instance with the {Executive} proxy to grant easy access
        # to components and protocols
        from .Client import Client
        Client.pyre_installExecutive(executive=self)

        # all done
        return


# end of file 
