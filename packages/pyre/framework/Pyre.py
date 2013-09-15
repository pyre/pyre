# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import weakref
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
        configurator.processEvents(events=events, priority=self.priority.command)

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

        # get storage for the framework manager proxies
        from .Client import Client as client

        # attach me
        client.pyre_executive = weakref.proxy(self)

        # build my nameserver
        self.nameserver = self.newNameServer()
        # attach
        client.pyre_nameserver = weakref.proxy(self.nameserver)

        # my fileserver
        self.fileserver = self.newFileServer()
        # attach
        client.pyre_fileserver = weakref.proxy(self.fileserver)

        # component bookkeeping
        self.registrar = self.newComponentRegistrar()
        # attach
        client.pyre_registrar = weakref.proxy(self.registrar)

        # handler of configuration events
        self.configurator = self.newConfigurator(executive=self)
        # attach
        client.pyre_configurator = weakref.proxy(self.configurator)

        # component linker
        self.linker = self.newLinker()
        # the timer registry
        self.timekeeper = self.newTimerRegistry()

        # the manager of external tools and libraries
        self.externals = self.newExternalsManager()
        # attach
        client.pyre_externals = weakref.proxy(self.externals)

        # all done
        return


# end of file 
