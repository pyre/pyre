# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Executive import Executive
from ..patterns.Singleton import Singleton


class Pyre(Executive, metaclass=Singleton):

    """
    The framework executive singleton
    """


    # the start up sequence
    def boot(self):
        """
        Perform all the default initialization steps
        """
        # install the default configuration settings
        import pyre
        self.calculator["pyre.home"] = pyre.home()
        self.calculator["pyre.prefix"] = pyre.prefix()

        # read and apply settings from the default configuration files
        for folder in self.configpath:
            source = self.fileserver.PATH_SEPARATOR.join([folder, self.bootup])
            try:
                self.loadConfiguration(uri=source, priority=self.BOOT_CONFIGURATION)
            except self.fileserver.NotFoundError as error:
                # ignore nonexistent files
                pass

        # process the command line
        import sys
        from . import newCommandLineParser
        # build a command line parser
        parser = newCommandLineParser()
        # parse the command line
        parser.decode(self.configurator, sys.argv[1:])
        # get the configurator to update my configuration
        self.configurator.configure(executive=self, priority=self.USER_CONFIGURATION)

        # ready to go
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize
        self.boot()
        return


    # constants
    bootup = "pyre.pml"


# end of file 
