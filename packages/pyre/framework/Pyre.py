# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Executive import Executive
from ..patterns.Singleton import Singleton


class Pyre(Executive, metaclass=Singleton):
    """
    The framework executive singleton
    """


    # the startup sequence
    def boot(self):
        """
        Perform all the default initialization steps
        """
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
        from . import newCommandLineParser
        # build the parser
        parser = newCommandLineParser()
        # register the local handlers
        parser.handlers["config"] = self._configurationLoader
        # return the parser
        return parser


    # clean up
    @classmethod
    def shutdown(cls):
        """
        Remove the reference to me held by the singleton
        """
        cls._pyre_singletonInstance = None
        return


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
