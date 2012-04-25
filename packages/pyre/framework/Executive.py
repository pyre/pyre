# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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


    # exceptions
    from .exceptions import FrameworkError, BadResourceLocatorError
    from .exceptions import ComponentNotFoundError, ShelfNotFoundError, SymbolNotFoundError
    from ..config.exceptions import DecodingError


    # public data
    configpath = ()
    # managers
    binder = None
    codex = None
    configurator = None
    fileserver = None
    registrar = None
    timekeeper = None
    resolvers = None

    # book keeping
    packages = None
    errors = None

    # constants
    defaultLocations = ("/pyre/system", "/pyre/user", "/local")
    path = tuple('vfs:' + location for location in defaultLocations)
    # priority levels for the various configuration sources
    from ..config.levels import ( 
        DEFAULT_CONFIGURATION, # defaults from the component declarations
        BOOT_CONFIGURATION, # configuration from the standard pyre boot files
        PACKAGE_CONFIGURATION, # configuration from package files
        USER_CONFIGURATION, # configurations supplied by the end user
        EXPLICIT_CONFIGURATION, # programmatic overrides
        )


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
        configuration = reader.decode(uri=uri, source=source, locator=locator)
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


    def registerNamespaceResolver(self, resolver, namespace):
        """
        Add {resolver} to the table of entities that get notified when an unqualified component
        resolution request is made

        For example, {pyre.shells.Director} registers an application class as a resolver of
        requests within the namespace specified by the application family. This way,
        unqualified requests for facility bindings can be resolved in an application specific
        manner. Look at {Executive.retrieveComponentDescriptor} for more details
        """
        # register the {resolver} under the key {namespace}
        self.resolvers[namespace] = resolver
        # and return
        return


    def translateSymbol(self, symbol, context):
        """
        Give registered namespace resolvers an opportunity to translate {symbol}
        """
        # check whether there is a registered resolver for this namespace
        resolver = self.locateNamespaceResolver(context)
        # if one has been registered
        if resolver:
            # let it translate the symbol
            return resolver.pyre_translateSymbol(symbol=symbol, context=context)
        # otherwise,  return the {symbol} as is
        return symbol


    def componentSearchPath(self, context):
        """
        Build a sequence of locations where component descriptors from {context} may be found
        """
        # check whether there is a registered resolver for this namespace
        resolver = self.locateNamespaceResolver(context)
        # if one has been registered
        if resolver:
            # let it provide appropriate locations
            for location in resolver.pyre_componentSearchPath(context):
                # to hand to our client
                yield location

        # now, go through the standard locations, in reverse order
        for location in reversed(self.defaultLocations):
            # starting with the full context path and shrinking
            for marker in reversed(range(1, len(context)+1)):
                # build and present a filename
                yield self.fileserver.join(location, *context[:marker])+'.py'

        # no more
        return


    def locateNamespaceResolver(self, context):
        """
        Attempt to locate a registered resolver for {context} namespaces
        """
        # print(" ** Executive.locateNamespaceResolver: context={!r}".format(context))
        # use the {context} to find the namespace resolver, starting with the full
        # {context} and progressively shrinking it
        for count in reversed(range(1, len(context)+1)):
            try:
                candidate = ".".join(context[:count])
                # print("    candidate: {!r}".format(candidate))
                return self.resolvers[candidate]
            # if there isn't one registered for this package
            except KeyError:
                # move on
                continue
        # otherwise
        return None


    # support for the various internal requests
    def configurePackage(self, package):
        """
        Locate and load the configuration files for the given {package}

        Typically, the package to which a component belongs can be deduced from its family
        name. This method will locate and load the package configuration files. These files are
        meant to allow site managers and end users to override the class wide defaults for the
        traits of the components in the package.
        
        This behavior is triggered by the first encountered component from each package, and it
        is done only once.
        """
        # if none were provided, there is no file-based configuration
        if not package: return package
        # also, bail out if this package has been configured previously
        if package in self.packages: return
        # we have a package name
        # print("Executive.configurePackage: configuring package {!r}".format(package))
        # form all possible filenames for the configuration files
        scope = itertools.product(self.configpath, [package], self.codex.getEncodings())
        # attempt to load the configuration settings
        for path, filename, extension in scope:
            # construct the actual filename
            source = self.fileserver.splice(path, filename, extension)
            # print("Executive.configurePackage: loading {!r}".format(source))
            # and try to load the configuration
            try:
                self.loadConfiguration(uri=source, priority=self.PACKAGE_CONFIGURATION)
            except self.fileserver.NotFoundError as error:
                continue
            # print("Executive.configurePackage: loaded {!r}".format(source))
        # in any case, this is the best that can be done for this package
        # update the set of known packages
        self.packages.add(package)
        # print("Executive.configurePackage: done; packages={}".format(self.packages))
        # all done
        return package


    def retrieveComponentDescriptor(self, uri, context=None, locator=None):
        """
        Interpret {uri} as a component descriptor and attempt to resolve it

        {uri} encodes the descriptor using the URI specification 
            scheme://authority/address#namme
        where 
            {scheme}: the resolution mechanism
            {authority}: the process that will perform the resolution
            {address}: the location of the component descriptor
            {name}: the optional name to use when instantiating the retrieved descriptor

        Currently, there is support for two classes of schemes:

        The "import" scheme requires that the component descriptor is accessible on the python
        path. The corresponding codec interprets {address} as two parts: {package}.{symbol},
        with {symbol} being the trailing part of {address} after the last '.'. The codec then
        uses the interpreter to import the symbol {symbol} using {address} to access the
        containing module. For example, the {uri}

            import:package.subpackage.module.myFactory

        is treated as if the following statement had been issued to the interpreter

            from package.subpackage.module import myFactory

        See below for the requirements myFactory must satisfy

        Any other scheme specification is interpreted as a request for a file based component
        factory. The {address} is again split into two parts: {path}/{symbol}, where {symbol}
        is the trailing part after the last '/' separator. The codec assumes that {path} is a
        valid path in the physical or logical filesystems managed by the executive.fileserver,
        and that it contains executable python code that provides the definition of the
        required symbol.  For example, the {uri}

            vfs:/local/sample.odb/myFactory

        expects that the fileserver can resolve the address local/sample.odb into a valid file
        within the virtual filesystem that forms the application namespace.

        The symbol referenced by the {symbol} fragment must be a callable that can produce
        component class records when called. For example

            def myFactory():
                import pyre
                class mine(pyre.component): pass
                return mine

        would be valid contents for an accessible module or an odb file.
        """
        # print(" ** Executive.retrieveComponentDescriptor:")
        # print("        uri: {!r}".format(uri))
        # print("        context: {!r}".format(context))
        # print("        shelves: {!r}".format(tuple(self.shelves.keys())))
        # make sure {context} is iterable
        context = context if context is not None else ()
        # pull out only, the currently supported parts; if parsing fails, it is a badly formed
        # request and an exception will get raised
        scheme, _, address, _, name = self.parseURI(uri)

        # if {uri} contains a scheme, use it; otherwise, try all the options
        schemes = [scheme] if scheme else ["vfs", "import"]
        # print("        schemes: {!r}".format(schemes))

        # iterate over the encoding possibilities
        for scheme in schemes:
            # print("          attempting {!r}".format(scheme))
            # attempt to
            try:
                # build a codec for this candidate scheme
                codec = self.codex.newCodec(encoding=scheme)
            # if the scheme is not known
            except KeyError:
                # construct the reason
                reason = "unknown scheme {!r}".format(scheme)
                # complain
                raise self.BadResourceLocatorError(uri=uri, reason=reason, locator=locator)

            # attempt to locate a component descriptor
            for descriptor in codec.locateSymbol(
                client=self,
                scheme=scheme, specification=address, context=context, locator=locator):
                # if there was no component name specified, return the descriptor
                if name is None: return descriptor
                # try to lookup a component by this name
                try:
                    return self.registrar.names[name]
                # if no such name has been registered
                except KeyError:
                    # build a component instance and return it
                    return descriptor(name=name)
                
        # if we get this far, everything we could try has failed
        raise self.ComponentNotFoundError(uri=uri, locator=locator)


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
        self.configurePackage(package=component.pyre_getPackageName())
        # populate the class defaults with the configuration information
        errors = self.configurator.configureComponentClass(self.registrar, component)
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
        errors = self.configurator.configureComponentInstance(self.registrar, component)
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


    # access to the shelf registry
    def registerShelf(self, shelf, source):
        """
        Record the {source} that corresponds to the given {shelf}
        """
        # add {source} to the dictionary with the loaded shelves
        self.shelves[source] = shelf
        # and return
        return self


    def loadShelf(self, uri, locator=None):
        """
        Load the contents of the shelf pointed to by {uri}

        {uri} encodes the descriptor using the URI specification 
            scheme://authority/address
        where
             scheme: one of import, file, vfs
             authority: currently not used; you may leave blank
             address: a scheme dependent specification of the location of the shelf
        """
        # parse the {uri}
        scheme, authority, address, query, symbol = self.parseURI(uri)
        # adjust the scheme, if necessary
        scheme = scheme.strip().lower() if scheme else 'file'
        # use the {scheme} to build a codec
        codec = self.codex.newCodec(encoding=scheme)
        # get it to hunt down candidates
        for shelf in codec.locateShelves(
            client=self, scheme=scheme, address=address, context=(), locator=locator):
            # i am only interested in the first hit
            return shelf
        # if no appropriate candidate was found
        raise self.ShelfNotFoundError(uri=uri)


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
        # the map of namespaces to the entities that resolve name requests
        self.resolvers = {}

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
