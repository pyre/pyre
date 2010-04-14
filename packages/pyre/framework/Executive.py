# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import pyre.framework


class Executive(object):

    """
    The top level framework object.

    Executive maintains the following suite of objects that provide the various mechanisms and
    policies that enable pyre applications:

        NYI:
    """


    # public data
    calculator = None # the manager of configuration nodes
    codecs = None # my codec manager
    configurator = None # my configuration manager
    curator = None # the manager of configuration sources
    fileserver = None # my virtual filesystem


    # interface
    def loadConfiguration(self, uri):
        """
        Load configuration settings from {uri}.
        """
        # ask the curator to decode the uri
        scheme, address, fragment = self.curator.parseURI(uri)
        # ask the fileserver to produce the input stream
        source = self.fileserver.open(scheme=scheme, address=address)
        # lookup the codec based on the file extension
        path, extension = os.path.splitext(address)
        reader = self.codecs.newCodec(encoding=extension[1:])
        # decode the configuration stream
        reader.decode(stream=source, configurator=self.configurator)
        # get the configurator to update the evaluation model
        self.configurator.populate(self.calculator)
        # all done
        return


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

        # the manager of configuration sources
        self.curator = pyre.framework.newCurator()
        # my configuration manager
        self.configurator = pyre.framework.newConfigurator()
        # the manager of configuration nodes
        self.calculator = pyre.framework.newCalculator()

        return


# end of file 
