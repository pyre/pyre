# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import re
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
    # paths
    configpath = ()
    # managers
    binder = None # responsible for the casting and validation of user input
    calculator = None # responsible for the framework evaluation model
    codecs = None # the registrar of configuration file parsers
    configurator = None # the accumulator of raw input from configuration sources
    fileserver = None # my virtual filesystem
    registrar = None # the component class and instance registrar
    # book keeping
    packages = () # the set of configured packages


    # constants
    path = ("vfs:///pyre/system", "vfs:///pyre/user", "vfs:///local")

    # priority levels for various configuration sources
    BOOT_CONFIGURATION = 0 # defaults from the component declarations
    PACKAGE_CONFIGURATION = 5 # configuration from package files
    USER_CONFIGURATION = 10 # configurations supplied by the end user
    EXPLICIT_CONFIGURATION = 15 # programmatic overrides


    # interface
    # retrieval
    def retrieveComponentDescriptor(self, uri):
        """
        Interpret {uri} as a component descriptor and attempt to resolve it

        {uri} encodes the descriptor using the URI specification 
            scheme://address#factory
        Currently, the two schemes that are supported are "import" and "file".

        The "import" scheme requires that the component descriptor is accessible on the python
        path. The corresponding codec uses the interpreter to import the symbol {factory} using
        {address} to access the containing module. For example, the {uri}

            import://package.subpackage.module#myFactory

        is treated as if the following statement had been issued to the interpreter

            from package.subpackage.module import myFactory

        See below for the requirements myFactory must satisfy

        The "file" scheme assumes that {address} is a valid path in the logical application
        namespace, managed by the executive.fileserver. The extension of the loical file is
        used to retrieve an apropriate decoder, which becomes responsible for retrieving the
        contents of the file and processing it. For example, the {uri}

            file:///local/sample.odb#myFactory

        expects that the fileserver can resolve the address local/sample.odb into a valid file,
        that there is a codec registered with the executive.codecs manager that can handle the
        odb encoding, and can produce the symbol myFactory

        The symbol referenced by the {factory} fragment must be a callable that can produce
        component instances given the name of the component instance as its sole argument. For
        example

            from pyre.components.Component import Component
            class mine(Component): pass
            def myFactory(name):
                return mine(name)

        would be valid contents for an accessible module or an odb file.
        """
        # parse the {uri}
        scheme, address, factory = self.parseURI(uri)
        # if the scheme is "import"
        if scheme == "import":
            # use the address as the shelf hash key
            key = address
            # build the codec
            codec = self.codecs.newCodec(encoding=scheme)
        # otherwise, expect the scheme to be "file"
        elif scheme == "file":
            # look up the adrress 
            vnode = self.fileserver[address]
            # split the address into two parts
            path,encoding = os.path.splitext(address)
            # use the extension to build the codec; don't forget to skip past the '.'
            codec = self.codecs.newCodec(encoding=encoding[1:])
        # otherwise, raise a firewall
        else:
            import journal
        #
        print(codec)
        # now decode the address
        shelf = codec.decode(address)
        print(shelf)


    # registration
    def registerComponentClass(self, component):
        """
        Register the {component} class record
        """
        # get the component class registered
        self.registrar.registerComponentClass(component)
        # invoke the class registration hook
        component.pyre_prepareClass(executive=self)
        # configure; do this before component class initialization
        self.loadPackageConfiguration(component)
        # transfer the configuration settings to the class properties
        self.calculator.configureComponentClass(executive=self, component=component)
        # invoke the class configuration hook
        component.pyre_configureClass(executive=self)
        # and hand back the class record
        return component


    def registerComponentInstance(self, component):
        """
        Register the {component} instance
        """
        # get the instance registered
        self.registrar.registerComponentInstance(component)
        # invoke the registration hook
        component.pyre_prepare(executive=self)
        # transfer the configuration settings to the instance properties
        self.calculator.configureComponentInstance(executive=self, component=component)
        # invoke the configuration hook
        component.pyre_configure(executive=self)
        # bind the configuration settings to the component
        # currently, this is a required step so that component instances can have their
        # properties propely cast to their native types
        # NYI: rethink this process
        self.binder.bindComponentInstance(executive=self, component=component)
        # invoke the binding hook
        component.pyre_bind(executive=self)
        # todo
        print("NYI: component instance initialization")
        # and hand the instance back
        return component


    def registerInterfaceClass(self, interface):
        """
        Register the given interface class record
        """
        # not much to do with interfaces
        # just forward the request to the component registar
        self.registrar.registerInterfaceClass(interface)
        # invoke the class registration hook
        interface.pyre_prepareClass(executive=self)
        # and hand back the interface class
        return interface


    # configuration
    def loadConfiguration(self, uri, priority, locator=None):
        """
        Load configuration settings from {uri}.
        """
        # decode the uri
        scheme, address, fragment = self.parseURI(uri)
        # get the fileserver to deduce the encoding and produce the input stream
        encoding, source = self.fileserver.open(scheme=scheme, address=address)
        # instantiate the requested reader
        reader = self.codecs.newCodec(encoding)
        # decode the configuration stream
        reader.decode(configurator=self.configurator, stream=source, locator=locator)
        # get the configurator to update the evaluation model
        self.configurator.configure(executive=self, priority=priority)
        # all done
        return


    # configuration and initialization of component classes
    def loadPackageConfiguration(self, component):
        """
        Locate and load the configuration files for the package to which {component} belongs

        If the package to which {component} belongs can be deduced from its family name, this
        method will locate and load the package configuration files. These files are meant to
        allow site managers and end users to override the class wide defaults for the traits of
        the components in the package.
        
        This behavior is triggered by the first encountered component from each package, and it
        is done only once.
        """
        # get the package that this component belongs to
        package = component.pyre_getPackageName()
        # if none were provided, there is no file-based configuration
        if not package: return
        # also, bail out if this package has been configured previously
        if package in self.packages: return
        # we have a package name
        # form all possible filenames for the configuration files
        scope = itertools.product(reversed(self.configpath), [package], self.codecs.getEncodings())
        # attempt to load the configuration settings
        for path, filename, extension in scope:
            # construct the actual filename
            source = self.fileserver.join(path, filename, extension)
            # and try to load the configuration
            try:
                self.loadConfiguration(source, priority=self.PACKAGE_CONFIGURATION)
            except self.fileserver.NotFoundError as error:
                pass

        # all done
        return component


    # utilities
    def parseURI(self, uri, defaultScheme="file"):
        """
        Extract the scheme, address and fragment from {uri}.
        """
        # run uri through the recognizer
        match = self._uriRecognizer.match(uri)
        # if it fails to match, it must be malformed (or my regex is bad...)
        if match is None:
            raise self.BadResourceLocatorError(uri=uri, reason="unrecognizable")
        # extract the scheme
        scheme = match.group("scheme") or defaultScheme
        scheme = scheme.strip().lower()
        # extract the addres
        address = match.group("address")
        # check that it's not blank
        if not address:
            raise self.BadResourceLocatorError(uri=uri, reason="missing address")
        # extract the fragment
        fragment = match.group("fragment")
        # and return the triplet
        return scheme, address, fragment


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
        # the trait binder
        self.binder = pyre.framework.newBinder()

        # prime the configuration folder list
        self.configpath = list(self.path)

        # the set of known packages
        self.packages = set()

        # all done
        return


    # exceptions
    from .exceptions import FrameworkError, BadResourceLocatorError


    # private data
    _uriRecognizer = re.compile(
        r"((?P<scheme>[^:]+)://)?(?P<address>[^#]*)(#(?P<fragment>.*))?"
        )

    # from http://regexlib.com/Search.aspx?k=URL
    r"""
    ^(?=[^&])
    (?:(?<scheme>[^:/?#]+):)?
    (?://(?<authority>[^/?#]*))?
    (?<path>[^?#]*)(?:\?(?<query>[^#]*))?
    (?:#(?<fragment>.*))?
    """


# end of file 
