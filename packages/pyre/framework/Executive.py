# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import itertools
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
    fileserver = None # my virtual filesystem
    registrar = None # the component class and instance registrar


    # interface
    # registration
    def registerComponentClass(self, component):
        """
        Register the {component} class record
        """
        # get the component class registered
        self.registrar.registerComponentClass(component)
        # configure
        self.configureComponentClass(component)
        # initialize the class traits
        print("NYI: component class trait initialization")

        # and hand back the class record
        return component


    def registerComponentInstance(self, component):
        """
        Register the {component} instance
        """
        # NYI: initialize component traits
        print("NYI: component instance registration and configuration")
        # get the instance registered
        self.registrar.registerComponentInstance(component)
        # and hand it back
        return component


    def registerInterfaceClass(self, interface):
        """
        Register the given interface class record
        """
        # not much to do with interfaces
        # just forward the request to the component registar
        return self.registrar.registerInterfaceClass(interface)


    # configuration
    def loadConfiguration(self, uri, locator=None):
        """
        Load configuration settings from {uri}.
        """
        # get the fileserver to deduce the encoding and produce the input stream
        encoding, source = self.fileserver.open(uri)
        # instantiate the requested reader
        reader = self.codecs.newCodec(encoding)
        # decode the configuration stream
        reader.decode(configurator=self.configurator, stream=source, locator=locator)
        # get the configurator to update the evaluation model
        self.configurator.configure(self)
        # all done
        return


    def configureComponentClass(self, component):
        """
        Locate and load the configuration files for the {component} class record.

        This is a specialized behavior that attempt to load configuration files derived from
        the component's _pyre_family and initialize the class wide properties by overriding the
        defaults supplied by the component's author
        """
        print("NYI: sort out configuration override")
        # get the package that this component belongs to
        package = component.pyre_getPackageName()
        # if none were provided, there is no file-based configuration
        if not package: return
        # form all possible filenames for the configuration files
        for path, filename, extension in itertools.product(
            self.configpath, [package], self.codecs.getEncodings()):
            # build the filename
            source = self.fileserver.join(path, filename, extension)
            # try to load the configuration
            try:
                self.loadConfiguration(source)
            except self.FrameworkError as error:
                pass
        # all done
        return component


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
        # the component registrar
        self.registrar = pyre.framework.newComponentRegistrar()

        # prime the configuration folder list
        self.configpath = list(self.path)

        # all done
        return


    # constants
    path = ("vfs:///pyre/system", "vfs:///pyre/user")


    # exceptions
    from . import FrameworkError


# end of file 
