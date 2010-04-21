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
        for source in self.curator.defaultSources:
            self.loadConfiguration(source)
        # process the command line
        import sys
        parser = newCommandLineParser()
        parser.decode(self, sys.argv[1:])
        # ready to go
        return


# end of file 
