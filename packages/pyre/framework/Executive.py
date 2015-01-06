# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import re
import weakref
import operator # for the sorting key
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
    from ..schemata import uri
    from .Priority import Priority as priority

    # constants
    hostmapkey = 'pyre.hostmap' # the key with the nicknames of known hosts


    # public data
    # the managers; patched during boot
    nameserver = None # entities accessible by name
    fileserver = None # the URI resolver
    registrar = None # protocol and component bookkeeping
    configurator = None # configuration sources and events
    linker = None # the pyre plug-in manager
    timekeeper = None # the timer registry
    externals = None # the manager of external tools and libraries

    # the runtime environment; patched during discovery
    host = None
    user = None
    terminal = None
    environ = None

    # bookkeeping
    errors = None # the pile of exceptions raised during booting and configuration


    # high level interface
    def loadConfiguration(self, uri, locator=None, priority=priority.user):
        """
        Load configuration settings from {uri} and insert them in the configuration database
        with the given {priority}.
        """
        # parse the {uri}
        uri = self.uri().coerce(uri)
        # attempt to
        try:
            # ask the file server for the input stream
            source = self.fileserver.open(uri=uri)
            # print(" -- found: {} ".format(uri))
        # if that fails
        except self.PyreError as error:
            # save it
            # self.errors.append(error)
            # and bail out
            return
        # ask the configurator to process the stream
        errors = self.configurator.loadConfiguration(
            uri=uri, source=source, locator=locator, priority=priority)
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
        # print("Executive.configure:")
        # print("    stem={}".format(stem))
        # print("    locator={}".format(locator))
        # print("    priority={}".format(priority))
        # access the fileserver
        fs = self.fileserver
        # and the configurator
        cfg = self.configurator
        # form all possible combinations of filename fragments for the configuration sources
        scope = itertools.product(reversed(cfg.configpath), [stem], cfg.encodings())
        # look for each one
        for root, filename, extension in scope:
            # build the uri
            uri = fs.splice(root.uri, filename, extension)
            # print(' ++ looking for {!r}'.format(uri))
            # load the settings from the associated file
            self.loadConfiguration(uri=uri, priority=priority, locator=locator)
        # all done
        return


    def resolve(self, uri, protocol=None, **kwds):
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
        uri = self.uri().coerce(uri)
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

        # if the address part is empty, do not go any further
        if not uri.address: return

        # make a locator
        locator = tracking.simple('while resolving {!r}'.format(uri.uri))
        # load the component recognizers
        from ..components.Actor import Actor as actor
        from ..components.Component import Component as component

        # the easy things didn't work out; look for matching descriptors
        for candidate in self.retrieveComponentDescriptor(uri=uri, protocol=protocol, **kwds):
            # if the candidate is neither a component class nor a component instance
            if not (isinstance(candidate, actor) or isinstance(candidate, component)):
                # it must be a foundry
                try:
                    # so invoke it
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


    def retrieveComponents(self, uri):
        """
        Retrieve all component classes from the shelf at {uri}
        """
        # get the shelf
        shelf = self.linker.loadShelf(executive=self, uri=uri)
        # and return its contents
        return shelf.items()


    def retrieveComponentDescriptor(self, uri, protocol, **kwds):
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
            # try splicing the family name of the {protocol} with the given address
            if protocol:
                # build the new address
                extended = nameserver.join(protocol.pyre_family(), address)
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
        yield from self.linker.resolve(executive=self, protocol=protocol, uri=uri, **kwds)

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


    def registerPackage(self, name, file):
        """
        Register a {pyre} package
        """
        # build a locator
        locator = tracking.here(level=1)
        # get the nameserver to build one
        package = self.nameserver.createPackage(name=name, locator=locator)
        # register it
        package.register(executive=self, file=file)
        # configure it
        package.configure(executive=self, locator=locator)

        # all done
        return package


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
        # build one
        linker = Linker(**kwds)
        # initialize it
        linker.prime(executive=self)
        # and return it
        return linker


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


    def newSchema(self, **kwds):
        """
        Build a new schema manager
        """
        # access the factory
        from .Schema import Schema
        # build one and return it
        return Schema(**kwds)


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
        # initialize my namespaces
        self.initializeNamespaces()
        # all done
        return self


    def activate(self):
        """
        Turn on the executive
        """
        # nothing to do here, for now...
        return self


    def discover(self, **kwds):
        """
        Discover what is known about the runtime environment
        """
        # grab my nameserver
        nameserver = self.nameserver
        # and my fileserver
        fileserver = self.fileserver

        # access the platform protocol
        from ..platforms import platform
        # get the host class record; the default value already contains all we could discover
        # about the type of machine we are running on
        host = platform().default

        # hunt down the distribution configuration file and load it
        # make a locator
        here = tracking.simple('while discovering the platform characteristics')
        # set the stem
        stem = 'pyre/platforms/{}'.format(host.distribution)
        # attempt to load any matching configuration files
        self.configure(stem=stem, priority=self.priority.user, locator=here)

        # set up an iterator over the map of known hosts, in priority order
        knownHosts = nameserver.find(pattern=self.hostmapkey, key=operator.attrgetter('priority'))
        # go through them
        for info, slot in knownHosts:
            # get the regular expression from the slot value
            regex = slot.value
            # if my hostname matches
            if re.match(regex, host.hostname):
                # extract the nickname as the last part of the key name
                host.nickname = nameserver.split(info.name)[-1]
                # we are done
                break
        # if there was no match
        else:
            # make the hostname be the nickname
            host.nickname = host.hostname

        # hunt down the host specific configuration file and load it
        # make a locator
        here = tracking.simple('while discovering the host characteristics')
        # set the stem
        stem = 'pyre/hosts/{}'.format(host.nickname)
        # attempt to load any matching configuration files
        self.configure(stem=stem, priority=self.priority.user, locator=here)

        # instantiate the host information store and attach it
        self.host = host(name='pyre.host')

        # now the user and the terminal
        from ..shells import user, terminal
        # instantiate them and attach them
        self.user = user(name='pyre.user')
        self.terminal = terminal.pyre_default()(name='pyre.terminal')

        # finally, the environment variables
        from .Environ import Environ
        # instantiate and attach
        self.environ = Environ(executive=self)

        # get the client base class
        from .Dashboard import Dashboard as dashboard

        # build weak references to the managers of the runtime environment
        dashboard.pyre_host = weakref.proxy(self.host)
        dashboard.pyre_user = weakref.proxy(self.user)

        # all done
        return self


    def initializeNamespaces(self):
        """
        Create and initialize the default namespace entries
        """
        # initialize my fileserver
        self.fileserver.initializeNamespace()
        # initialize my configurator
        self.configurator.initializeNamespace()
        # all done
        return self


    # helpers and other details not normally useful to end users
    def _configurationLoader(self, key, value, locator):
        """
        Handler for the {config} command line argument
        """
        # load the configuration
        self.loadConfiguration(uri=value, locator=locator, priority=self.priority.command)
        # and return
        return


# end of file
