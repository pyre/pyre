# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import weakref
import itertools # for product
from .. import tracking


#  the class declaration
class Executive:
    """
    The specification of the obligations of the various managers of framework services
    """


    # exceptions
    from .exceptions import PyreError, ComponentNotFoundError

    # types
    from ..schema.URI import URI as uri
    from .Priority import Priority as priority


    # public data
    # the managers
    nameserver = None # entities accessible by name
    fileserver = None # the URI resolver
    registrar = None # protocol and component bookkeeping
    configurator = None # configuration sources and events
    linker = None # the pyre plug-in manager
    timekeeper = None # the timer registry
    externals = None # the manager of external tools and libraries

    # the runtime environment; patched during boot
    host = None 

    # bookkeeping
    errors = None # the pile of exceptions raised during booting and configuration


    # high level interface
    def loadConfiguration(self, uri, locator=None, priority=priority.user):
        """
        Load configuration settings from {uri} and insert them in the configuration database
        with the given {priority}.
        """
        # parse the {uri}
        uri = self.uri.coerce(uri)
        # attempt to
        try:
            # ask the file server for the input stream
            source = self.fileserver.open(uri=uri)
        # if that fails
        except self.PyreError as error:
            # save it
            # self.errors.append(error)
            # and bail out
            return
        # ask the configurator to process the stream
        errors = self.configurator.loadConfiguration(
            executive=self, uri=uri, source=source, locator=locator, priority=priority)
        # add any errors to my pile
        # self.errors.extend(errors)
        # all done
        return


    # other facilities
    def newTimer(self, **kwds):
        """
        Build an return a timer
        """
        # let the timer registry do its thing
        return self.timekeeper.timer(**kwds)


    # support for internal requests
    def configure(self, stem, locator, priority):
        """
        Locate and load all accessible configuration files for the given {stem}
        """
        # access the fileserver
        fs = self.fileserver
        # and the configurator
        cfg = self.configurator
        # form all possible combinations of filename fragments for the configuration sources
        scope = itertools.product(cfg.configpath, [stem], cfg.encodings())
        # look for each one
        for root, filename, extension in scope:
            # build the uri
            uri = fs.splice(root, filename, extension)
            # load the settings from the associated file
            self.loadConfiguration(uri=uri, priority=priority, locator=locator)
        # all done
        return


    def configurePackage(self, package, locator):
        """
        Locate and load the configuration files for the given {package}
        """
        # delegate
        return self.configure(stem=package.name, priority=self.priority.package, locator=locator)
        

    def resolve(self, uri, client=None, **kwds):
        """
        Interpret {uri} as a component descriptor and attempt to resolve it

        {uri} encodes the descriptor using the URI specification 
            scheme://authority/address#name
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

            import:gauss.shapes.box

        is treated as if the following statement had been issued to the interpreter

            from gauss.shapes import box

        See below for the requirements myFactory must satisfy

        Any other scheme specification is interpreted as a request for a file based component
        factory. The {address} is again split into two parts: {path}/{symbol}, where {symbol}
        is the trailing part after the last '/' separator. The codec assumes that {path} is a
        valid path in the physical or logical filesystems managed by the
        {executive.fileserver}, and that it contains executable python code that provides the
        definition of the required symbol.  For example, the {uri}

            vfs:/local/shapes.odb/box

        implies that the fileserver can resolve the address {local/shapes.odb} into a valid
        file within the virtual filesystem that forms the application namespace. The symbol
        referenced by the {symbol} fragment must be a callable that can produce component class
        records when called. For example, the file {shapes.odb} might contain

            import pyre
            class box(pyre.component): pass

        which exposes a component class {box} that has the right name and whose constructor can
        be invoked to produce component instances. If you prefer to place such declarations
        inside functions, e.g. to avoid certain name collisions, you can use constructs such as

            def box():
                import pyre
                class box(pyre.component): pass
                return box
        """
        # force a uri
        uri = self.uri.coerce(uri)
        # grab my nameserver
        nameserver = self.nameserver

        # if the {uri} contains a fragment, treat it as the name of the component
        name = uri.fragment

        # is there anything registered under it? check carefully: do not to disturb the symbol
        # table of the nameserver, in case the name is junk
        if name and name in nameserver:
            # look it up
            try:
                # and return it
                yield nameserver[name]
            # if it is unresolved
            except nameserver.UnresolvedNodeError:
                # no worries
                pass

        # make a locator
        locator = tracking.simple('while resolving {!r}'.format(uri.uri))
        # load the component recognizers
        from ..components.Actor import Actor as actor
        from ..components.Component import Component as component

        # the easy things didn't work out; look for matching descriptors
        for candidate in self.retrieveComponentDescriptor(uri=uri, client=client, **kwds):
            # if the candidate is neither a component class nor a component instance
            if not (isinstance(candidate, actor) or isinstance(candidate, component)):
                # it must be a callable the returns one
                try:
                    # evaluate it
                    candidate = candidate()
                # if this fails
                except TypeError:
                    # move on to the next candidate
                    continue
                # if it succeeded, verify it is a component
                if not (isinstance(candidate, actor) or isinstance(candidate, component)):
                    # and if not, move on
                    continue
            # if it is a component class and we have been asked to instantiate it
            if name and isinstance(candidate, actor):
                # build it
                candidate = candidate(name=name, locator=locator)
            # otherwise
            else:
                # just mark it
                candidate.pyre_locator = tracking.chain(candidate.pyre_locator, locator)
            # ready to  hand it to our caller
            yield candidate

        # totally out of ideas
        return


    def retrieveComponentDescriptor(self, uri, client, **kwds):
        """
        The component resolution workhorse
        """
        # grab my nameserver
        nameserver = self.nameserver
        # get the uri scheme
        scheme = uri.scheme
        # and the address
        address = uri.address
        # if no {scheme} was specified, assume it is {import} and look for possible
        # interpretation of the uri that have been loaded previously
        if not scheme:
            # check whether the {address} points to a component that has been loaded
            # previously; if there
            if address and address in nameserver:
                # look it up
                try:
                    # and return it
                    yield nameserver[address]
                # if it is unresolved
                except nameserver.UnresolvedNodeError:
                    # no worries
                    pass
            # try splicing the family name of the {client} with the given address
            if client:
                # build the new address
                extended = nameserver.join(client.schema.pyre_family(), address)
                # does the nameserver recognize it?
                if extended in nameserver:
                    # look it up
                    try:
                        # and return it
                        yield nameserver[extended]
                    # if it is unresolved
                    except nameserver.UnresolvedNodeError:
                        # no worries
                        pass

        # ask the linker to find descriptors
        yield from self.linker.resolve(executive=self, client=client, uri=uri, **kwds)

        # all done
        return


    # registration interface for framework objects
    def registerProtocolClass(self, protocol, family, locator):
        """
        Register a freshly minted protocol class
        """
        # make a locator
        pkgloc = tracking.simple('while registering protocol {!r}'.format(family))
        # get the associated package
        package = self.nameserver.package(executive=self, name=family, locator=pkgloc)
        # associate the protocol with its package
        package.protocols.add(protocol)
        # insert it into the model
        key = self.nameserver.configurable(name=family, configurable=protocol, locator=locator)
        # and return the nameserver registration key
        return key


    def registerComponentClass(self, component, family):
        """
        Register a freshly minted component class
        """
        # make a locator
        pkgloc = tracking.simple('while registering component {!r}'.format(family))
        # get the associated package
        package = self.nameserver.package(executive=self, name=family, locator=pkgloc)
        # associate the component with its package
        package.components.add(component)
        # get the component locator
        locator = component.pyre_locator
        # insert the component into the model
        key = self.nameserver.configurable(name=family, configurable=component, locator=locator)
        # return the key
        return key


    def registerComponentInstance(self, instance, name):
        """
        Register a freshly minted component instance
        """
        # get the instance locator
        locator = instance.pyre_locator
        # insert the component instance into the model
        key = self.nameserver.configurable(name=name, configurable=instance, locator=locator)
        # return the key
        return key


    # the default factories of all my parts
    def newNameServer(self, **kwds):
        """
        Build a new name server
        """
        # access the factory
        from .NameServer import NameServer
        # build one and return it
        return NameServer(**kwds)


    def newFileServer(self, **kwds):
        """
        Build a new file server
        """
        # access the factory
        from .FileServer import FileServer
        # build one and return it
        return FileServer(**kwds)


    def newComponentRegistrar(self, **kwds):
        """
        Build a new component registrar
        """
        # access the factory
        from ..components.Registrar import Registrar
        # build one and return it
        return Registrar(**kwds)


    def newConfigurator(self, **kwds):
        """
        Build a new configuration event processor
        """
        # access the factory
        from ..config.Configurator import Configurator
        # build one and return it
        return Configurator(**kwds)


    def newLinker(self, **kwds):
        """
        Build a new configuration event processor
        """
        # access the factory
        from .Linker import Linker
        # build one and return it
        return Linker(**kwds)


    def newCommandLineParser(self, **kwds):
        """
        Build a new parser of command line arguments
        """
        # access the factory
        from ..config.CommandLineParser import CommandLineParser
        # build one
        parser = CommandLineParser(**kwds)
        # register the local handlers 
        parser.handlers['config'] = self._configurationLoader
        # and return the parser
        return parser


    def newTimerRegistry(self, **kwds):
        """
        Build a new time registrar
        """
        # access the factory
        from ..timers.Registrar import Registrar
        # build one and return it
        return Registrar(**kwds)


    def newExternalsManager(self, **kwds):
        """
        Build a new manager for external tools and libraries available to pyre applications
        """
        # access the factory
        from .Externals import Externals
        # build one and return it
        return Externals(**kwds)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the pile of errors encountered
        self.errors = []
        # all done
        return


    # implementation details
    def boot(self):
        """
        Perform the final framework initialization step
        """
        # initialize my namespace
        self.initializeNamespace()
        # all done
        return self


    def discover(self, **kwds):
        """
        Discover what is known about the runtime environment
        """
        # access the platform protocol
        from ..platforms import platform
        # get information about the current host
        self.host = platform().default(name='pyre.host')

        # all done
        return self


    def initializeNamespace(self):
        """
        Create and initialize the default namespace entries
        """
        # ask my configurator for its defaults
        self.configurator.initializeNamespace(nameserver=self.nameserver)

        # all done
        return self


    # helpers and other details not normally useful to end users
    def _configurationLoader(self, key, value, locator):
        """
        Handler for the {config} command line argument
        """
        # load the configuration
        self.loadConfiguration(uri=value, locator=locator, priority=self.priority.user)
        # and return
        return


# end of file 
