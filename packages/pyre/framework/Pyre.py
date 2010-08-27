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


    # the startup sequence
    def boot(self):
        """
        Perform all the default initialization steps
        """
        # process the command line
        import sys
        from . import newCommandLineParser
        # build a command line parser
        parser = newCommandLineParser()
        # parse the command line
        configuration = parser.decode(sys.argv[1:])
        # get the configurator to update my configuration
        self.configurator.configure(configuration=configuration, priority=self.USER_CONFIGURATION)

        # read and apply settings from the default configuration files
        for folder in self.configpath:
            for configfile  in self.bootconf:
                source = self.fileserver.PATH_SEPARATOR.join([folder, configfile])
                # print("Pyre.boot: loading {!r}".format(source))
                try:
                    self.loadConfiguration(uri=source, priority=self.BOOT_CONFIGURATION)
                except self.fileserver.NotFoundError as error:
                    # print("Pyre.boot: {!r} not found".format(source))
                    # ignore non-existent files
                    pass
        # ready to go
        return self


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize
        self.boot()
        return


    # constants
    bootconf = ("pyre.pml",)


# end of file 
