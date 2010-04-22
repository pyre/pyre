# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Executive import Executive
from ..patterns.Singleton import Singleton

from . import newCommandLineParser


class Pyre(Executive, metaclass=Singleton):

    """
    The framework executive singleton
    """


    # the start up sequence
    def boot(self):
        """
        Perform all the default initialization steps
        """
        # read and apply settings from the default configuration files
        for folder in self.configpath:
            source = self.fileserver.PATH_SEPARATOR.join([folder, self.bootup])
            try:
                self.loadConfiguration(source)
            except self.FrameworkError as error:
                # something bad happened
                # NYI: log an informational with journal and move on
                # print(error)
                pass

        # process the command line
        import sys
        parser = newCommandLineParser()
        parser.decode(self, sys.argv[1:])

        # get the configurator to update my configuration
        self.configurator.configure(self)

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
