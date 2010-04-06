# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre.framework


class Executive(object):

    """
    The top level framework object.

    Executive maintains the following suite of objects that provide the various mechanisms and
    policies that enable pyre applications:

        NYI:
    """


    # public data
    codecs = None # my codec manager
    fileserver = None # my virtual filesystem
    configurator = None # my configuration manager
    calculator = None # the manager of configuration nodes


    # start up interface
    def boot(self):
        """
        Perform all the default initialization steps
        """


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # my codec manager
        self.codecs = pyre.framework.newCodecManager()
        # my virtual filesystem
        self.fileserver = pyre.framework.newFileServer()
        # my configuration manager
        self.configurator = pyre.framework.newConfigurator()
        # the manager of configuration nodes
        self.calculator = pyre.framework.newCalculator()

        return


# end of file 
