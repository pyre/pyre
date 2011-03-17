# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import os
import re
import itertools


class Executive:
    """
    The top level framework object

    This class maintains a suite of managers that are responsible for the various mechanisms
    and policies that enable pyre applications. The Executive orchestrates their interactions
    and provides the top level interface of the framework.

    The actual executive is an instance of the class Pyre, also in this package. Pyre is a
    singleton that is accessible as pyre.executive. For more details, see Pyre.py and
    __init__.py in this package.
    """


    # public data
    configpath = ()
    # managers
    binder = None
    codex = None
    configurator = None
    fileserver = None
    registrar = None
    timekeeper = None
    # book keeping
    packages = None
    errors = None

    # constants
    path = ("vfs:///pyre/system", "vfs:///pyre/user", "vfs:///local")
    # priority levels for the various configuration sources
    DEFAULT_CONFIGURATION = -1 # defaults from the component declarations
    BOOT_CONFIGURATION = 0 # configuration from the standard pyre boot files
    PACKAGE_CONFIGURATION = 5 # configuration from package files
    USER_CONFIGURATION = 10 # configurations supplied by the end user
    EXPLICIT_CONFIGURATION = 15 # programmatic overrides


    # external interface
    def loadConfiguration(self, uri, priority=USER_CONFIGURATION, locator=None):
        """
        Load configuration settings from {uri} and insert them in the configuration database
        with the given {priority}.
        """
        # decode the uri
        scheme, authority, address, query, fragment = self.parseURI(uri)
        # get the fileserver to  deduce the encoding and produce the input stream
        encoding, source = self.fileserver.open(scheme, address=address)
        # instantiate the requested reader
        reader = self.codex.newCodec(encoding)
        # extract the configuration setting from the source
        configuration = reader.decode(source=source, locator=locator)
        # update the evaluation model
        errors = self.configurator.configure(configuration=configuration, priority=priority)
        # add any errors to the pile
        self.errors.extend(errors)
        # all done
        return self


    # other facilities
    def newTimer(self, **kwds):
        """
        Build and return a timer
        """
        # let the timer registry do its thing
        return self.timekeeper.timer(**kwds)


    # support for the various internal requests
    def retrieveComponentDescriptor(self, uri, locator=None):
        """
        Interpret {uri} as a component descriptor and attempt to resolve it

        {uri} encodes the descriptor using the URI specification 
            scheme://authority/address#symbol
        Currently, there is support for two classes of schemes.

        The "import" scheme requires that the component descriptor is accessible on the python
        path. The corresponding codec uses the interpreter to import the symbol {symbol} using
        {address} to access the containing module. For example, the {uri}

            import:package.subpackage.module#myFactory

        is treated as if the following statement had been issued to the interpreter

            from package.subpackage.module import myFactory

        See below for the requirements myFactory must satisfy

        Any other scheme specification is interpreted as a request for a file based component
        factory. The executive assumes that {address} is a valid path in the physical or
        logical filesystems managed by the executive.fileserver, and that it contains
        executable python code the provides the definition of the required symbol.  For
        example, the {uri}

            vfs:///local/sample.odb#myFactory

        expects that the fileserver can resolve the address local/sample.odb into a valid file
        within the virtual filesystem that forms the application namespace.

        The symbol referenced by the {symbol} fragment must be a callable that can produce
        component class records when called. For example

            from pyre.components.Component import Component
            class mine(Component): pass
            def myFactory():
                return mine

        would be valid contents for an accessible module or an odb file.
        """
        # parse the {uri}
        scheme, authority, address, query, symbol = self.parseURI(uri)
        # print("Executive:retrieveComponentDescriptor: scheme={!r}, address={!r}, symbol={!r}".
              # format(scheme, address, symbol))

        # make some adjustments
        if scheme:
            scheme = scheme.strip().lower()
        else:
            scheme = 'file'

        # if the scheme is "import"
        if scheme == "import":
            # use the address as the shelf hash key
            source = address
            # build the codec
            codec = self.codex.newCodec(encoding="import")
        # otherwise, assume the source points to a file with python code
        else:
            # build a unique identifier for this source
            source = (scheme, address)
            # build the codec
            codec = self.codex.newCodec(encoding="odb", filesystem=self.fileserver)

        # check whether we have processed this source before
        try:
            # get the shelf
            shelf = self.shelves[source]
        # nope, it's the first time
        except KeyError:
            # extract the shelf
            shelf = codec.decode(source=source, locator=locator)
            # and cache it
            self.shelves[source] = shelf

        # now, retrieve the descriptor
        descriptor = codec.retrieveSymbol(shelf=shelf, symbol=symbol)
        # and return it
        return descriptor
            

    def loadPackageConfiguration(self, package):
        """
        Locate and load the configuration files for the package to which {component} belongs

        If the package to which {component} belongs can be deduced from its family name, this
        method will locate and load the package configuration files. These files are meant to
        allow site managers and end users to override the class wide defaults for the traits of
        the components in the package.
        
        This behavior is triggered by the first encountered component from each package, and it
        is done only once.
        """
        # if none were provided, there is no file-based configuration
        if not package: return package
        # also, bail out if this package has been configured previously
        if package in self.packages: return
        # we have a package name
        # print("Executive.loadPackageConfiguration: configuring package {!r}".format(package))
        # form all possible filenames for the configuration files
        scope = itertools.product(reversed(self.configpath), [package], self.codex.getEncodings())
        # attempt to load the configuration settings
        for path, filename, extension in scope:
            # construct the actual filename
            source = self.fileserver.join(path, filename, extension)
            # and try to load the configuration
            try:
                self.loadConfiguration(uri=source, priority=self.PACKAGE_CONFIGURATION)
            except self.fileserver.NotFoundError as error:
                continue
            # print("Executive.loadPackageConfiguration: loaded {!r}".format(source))
        # in any case, this is the best that can be done for this package
        # update the set of known packages
        self.packages.add(package)
        # print("Executive.loadPackageConfiguration: done; packages={}".format(self.packages))
        # all done
        return package


    # registration of configurables
    def registerComponentClass(self, component):
        """
        Register the {component} class record
        """
        # register the component
        self.registrar.registerComponentClass(component)
        # invoke the registration hook
        component.pyre_registerClass(executive=self)
        # load the package configuration; must do this before configuring the class
        self.loadPackageConfiguration(package=component.pyre_getPackageName())
        # populate the class defaults with the configuration information
        errors = self.configurator.configureComponentClass(component)
        # add any errors encountered to the pile
        self.errors.extend(errors)
        # invoke the configuration hook
        component.pyre_configureClass(executive=self)
        # bind the component
        self.binder.bindComponentClass(component)
        # invoke the initialization hook
        component.pyre_initializeClass(executive=self)
        # and hand back the class record
        return component


    def registerComponentInstance(self, component):
        """
        Register the {component} instance
        """
        # register the component instance
        self.registrar.registerComponentInstance(component)
        # invoke the registration hook
        component.pyre_register(executive=self)
        # configure it
        errors = self.configurator.configureComponentInstance(component)
        # add any errors encountered to the pile
        self.errors.extend(errors)
        # invoke the configuration hook
        component.pyre_configure(executive=self)
        # bind the component
        self.binder.bindComponentInstance(component)
        # invoke the binding hook
        component.pyre_bind(executive=self)
        # invoke the initialization hook
        component.pyre_initialize(executive=self)
        # and hand the instance back to the caller
        return component


    def registerInterfaceClass(self, interface):
        """
        Register the {interface} class record
        """
        # register the interface
        self.registrar.registerInterfaceClass(interface)
        # invoke the registration hook
        interface.pyre_registerClass(executive=self)
        # and hand back the class record
        return interface


    # utilities
    def parseURI(self, uri):
        """
        Extract the scheme, address and fragment from {uri}.
        """
        # run uri through the recognizer
        match = self._uriRecognizer.match(uri)
        # if it fails to match, it must be malformed (or my regex is bad...)
        if match is None:
            raise self.BadResourceLocatorError(uri=uri, reason="unrecognizable")
        # extract the scheme
        scheme = match.group("scheme")
        # extract the authority
        authority = match.group("authority")
        # extract the address
        address = match.group("address")
        # extract the query
        query = match.group("query")
        # extract the fragment
        fragment = match.group("fragment")
        # and return the triplet
        return scheme, authority, address, query, fragment


    # meta methods
    def __init__(self, managers, **kwds):
        super().__init__(**kwds)

        # the timer manager
        self.timekeeper = managers.newTimerRegistrar()
        # build and start a timer
        self.timer = self.timekeeper.timer(name="pyre").start()

        # the manager of the component interdependencies
        self.binder = managers.newBinder()
        # my codec manager
        self.codex = managers.newCodecManager()
        # my configuration manager
        self.configurator = managers.newConfigurator(executive=self)
        # the manager of my virtual filesystem
        self.fileserver = managers.newFileServer()
        # the component registrar
        self.registrar = managers.newComponentRegistrar()

        # prime the configuration folder list
        self.configpath = list(self.path)

        # initialize the set of known packages
        self.packages = set()

        # initialize the list of errors encountered during configuration
        self.errors = []

        # initialize the set of known configuration sources
        self.shelves = {}

        # all done
        return


    # exceptions
    from .exceptions import FrameworkError, BadResourceLocatorError
    from ..config.exceptions import DecodingError


    # private data
    _uriRecognizer = re.compile(
        "".join(( # adapted from http://regexlib.com/Search.aspx?k=URL
                r"^(?=[^&])", # disallow '&' at the beginning of uri
                r"(?:(?P<scheme>[^:/?#]+):)?", # grab the scheme
                r"(?://(?P<authority>[^/?#]*))?", # grab the authority
                r"(?P<address>[^?#]*)", # grab the address, typically a path
                r"(?:\?(?P<query>[^#]*))?", # grab the query, i.e. the ?key=value&... chunks
                r"(?:#(?P<fragment>.*))?"
                )))


# end of file 
