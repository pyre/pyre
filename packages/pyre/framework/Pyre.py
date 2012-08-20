# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Executive import Executive


# my declaration
class Pyre(Executive):
    """
    The framework executive singleton
    """


    # the startup sequence
    def boot(self):
        """
        Perform all the default initialization steps
        """
        # attach my managers

        # the timer manager
        from ..timers import newTimerRegistrar
        self.timekeeper = newTimerRegistrar()
        # build and start a timer
        self.timer = self.timekeeper.timer(name="pyre").start()

        # the manager of the component interdependencies
        from .Binder import Binder
        self.binder = Binder()
        # my codec manager
        from ..config import newCodecManager
        self.codex = newCodecManager()
        # my configuration manager
        from ..config import newConfigurator
        self.configurator = newConfigurator(executive=self)
        # the manager of my virtual filesystem
        from .FileServer import FileServer
        self.fileserver = FileServer()
        # the component registrar
        from ..components import newRegistrar
        self.registrar = newRegistrar()

        # patch the component infrastructure
        import weakref
        # patch Requirement
        from ..components import requirement
        requirement.pyre_executive = weakref.proxy(self)
        # patch Configurable
        from ..components import configurable
        configurable.pyre_executive = weakref.proxy(self)
        configurable.pyre_SEPARATOR = self.configurator.separator

        # process the command line
        import sys
        # build a command line parser
        parser = self.newCommandLineParser()
        # parse the command line
        commandline = parser.decode(sys.argv[1:])
        # get the configurator to update my configuration
        self.configurator.configure(configuration=commandline, priority=self.USER_CONFIGURATION)

        # read and apply settings from the default configuration files
        for package in self.defaultPackages:
            self.configurePackage(package)

        # ready to go
        return self


    # factories and initializers of framework objects
    def newCommandLineParser(self):
        """
        Build and initialize a new command line parser
        """
        # access the factory
        from ..config import newCommandLineParser
        # build the parser
        parser = newCommandLineParser()
        # register the local handlers
        parser.handlers["config"] = self._configurationLoader
        # return the parser
        return parser


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize
        self.boot()
        return


    # implementation details
    def _configurationLoader(self, key, value, locator):
        """
        Handler for the {config} command line argument
        """
        # load the configuration
        self.loadConfiguration(uri=value, locator=locator, priority=self.USER_CONFIGURATION)
        # and return
        return

    # constants
    defaultPackages = ("pyre",)


# end of file 
