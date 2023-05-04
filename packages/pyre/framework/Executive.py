# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import re
import weakref
import operator
import itertools

# primitives, locators
from .. import timers
from .. import primitives
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

    # get the client base class
    from .Dashboard import Dashboard as dashboard

    # constants
    hostmapkey = "pyre.hostmap"  # the key with the nicknames of known hosts

    # public data
    # the managers; patched during boot
    nameserver = None  # entities accessible by name
    fileserver = None  # the URI resolver
    registrar = None  # protocol and component bookkeeping
    configurator = None  # configuration sources and events
    linker = None  # the pyre plug-in manager

    # the runtime environment; patched during discovery
    host = None
    user = None
    terminal = None
    environ = None

    # bookkeeping
    errors = None  # the pile of exceptions raised during booting and configuration

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
            # print(f" -- found: {uri} ")
        # if that fails
        except self.PyreError as error:
            # save it
            self.errors.append(error)
            # and bail out
            return
        # ask the configurator to process the stream
        errors = self.configurator.loadConfiguration(
            uri=uri, source=source, locator=locator, priority=priority
        )
        # add any errors to my pile
        self.errors.extend(errors)
        # all done
        return

    # other facilities
    def newTimer(self, **kwds):
        """
        Build and return a timer
        """
        # let the timer registry do its thing
        return timers.wall(**kwds)

    # support for internal requests
    def configure(self, namespace, locator):
        """
        Locate and load all accessible configuration files for the given {namespace}
        """
        # first up, package level configuration based on the raw {namespace}; first in the
        # raw directory
        self.configureStem(
            stem=namespace, locator=locator, priority=self.priority.package
        )
        # and then in the private subdirectory
        stem = f"{namespace}/{namespace}"
        # locate and load
        self.configureStem(stem=stem, locator=locator, priority=self.priority.package)

        # next, we look for platform, machine, and user specific settings
        # get the host
        host = self.host
        # if it hasn't been identified yet
        if host is None:
            # none of what follows can be done, so bail
            return

        # we care about the os distribution
        distro = host.distribution
        # and the host nickname
        nickname = host.nickname
        # form the user tag
        user = f"{self.user.username}@{nickname}"

        # look for platform specific settings in a private subdirectory
        action = tracking.simple("while discovering the host characteristics")
        # chain to the existing locator
        chain = tracking.chain(action, locator)
        # first in the raw directory
        self.configureStem(stem=distro, priority=self.priority.user, locator=chain)
        # but also in the private subdirectory
        stem = f"{namespace}/platforms/{distro}"
        # attempt to load any matching configuration files
        self.configureStem(stem=stem, priority=self.priority.user, locator=chain)

        # look for host specific settings
        action = tracking.simple("while discovering the host characteristics")
        # chain to the existing locator
        chain = tracking.chain(action, locator)
        # first in the raw directory
        self.configureStem(stem=nickname, priority=self.priority.user, locator=chain)
        # but also in the private directory
        stem = f"{namespace}/hosts/{nickname}"
        # attempt to load any matching configuration files
        self.configureStem(stem=stem, priority=self.priority.user, locator=chain)

        # finally, look for a {user@host} configuration files
        action = tracking.simple("while loading the user specific configuration")
        # chain to the existing locator
        chain = tracking.chain(action, locator)
        # first in the raw directory
        self.configureStem(stem=user, priority=self.priority.user, locator=chain)
        # but also in the private directory
        stem = f"{namespace}/users/{user}"
        # attempt to load any matching configuration files
        self.configureStem(stem=stem, priority=self.priority.user, locator=chain)

        # all done
        return

    def configureStem(self, stem, locator, cfgpath=None, priority=priority.package):
        """
        Locate and load all accessible configuration files for the given {stem}
        """
        # show me
        # print("Executive.configureStem:")
        # print(f"    stem={stem}")
        # print(f"    cfgpath={cfgpath}")
        # print(f"    locator={locator}")
        # print(f"    priority={priority}")

        # get the name server
        ns = self.nameserver
        # and the configurator
        cfg = self.configurator

        # if the caller didn't supply a specific path of interest
        if cfgpath is None:
            # use the default
            cfgpath = reversed(ns.configpath)

        # form all possible combinations of filename fragments for the configuration sources
        scope = itertools.product(cfgpath, [stem], cfg.encodings())
        # look for each one
        for root, filename, extension in scope:
            # build the {uri}
            uri = f"{root}/{filename}.{extension}"
            # show me
            # print(f" ++ looking for '{uri}'")
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
        uses the interpreter to import the {symbol} using {address} to access the containing
        module. For example, the {uri}

            import:gauss.shapes.box

        is treated as if the following statement had been issued to the interpreter

            from gauss.shapes import box

        Any other scheme specification is interpreted as a request for a file based component
        factory. The {address} is again split into two parts: {path}/{symbol}, where {symbol}
        is the trailing part after the last '/' separator. The codec assumes that {path} is a
        valid path in the physical or logical filesystems managed by the
        {executive.fileserver}, and that it contains executable python code that provides the
        definition of the required symbol.  For example, the {uri}

            vfs:/local/shapes.py/box

        implies that the file server can resolve the address {local/shapes.py} into a valid file
        within the virtual filesystem that forms the application namespace. The referenced
        {symbol} must be a callable that can produce component class records when called. For
        example, the file {shapes.py} might contain

            import pyre
            class box(pyre.component): pass

        which exposes a component class {box} that has the right name and whose constructor can
        be invoked to produce component instances. If you prefer to place such declarations
        inside functions, e.g. to avoid certain name collisions, you can use mark your function
        as a component {foundry} by decorating as follows:

            @pyre.foundry(implements=())
            def box():
                class box(pyre.component): pass
                return box
        """
        # print('pyre.framework.Executive.resolve:')
        # print(f'    uri: {uri}')
        # print(f'    protocol: {protocol}')
        # force a uri
        uri = self.uri().coerce(uri)
        # grab my name server
        nameserver = self.nameserver

        # if the {uri} contains a fragment, treat it as the name of the component
        name = uri.fragment
        # is there anything registered under it? check carefully: do not to disturb the symbol
        # table of the name server, in case the name is junk
        if name and name in nameserver:
            # the name is known; attempt to
            try:
                # look up the corresponding entity
                candidate = nameserver[name]
            # if it is unresolved
            except nameserver.UnresolvedNodeError:
                # no worries; someone else has asked for it too, but it has not been realized yet
                pass
            # if it's there
            else:
                # send it off
                yield candidate
                # this is the only acceptable match; we are done
                return

        # if the address part is empty, do not go any further
        if not uri.address:
            return

        # load the component recognizers
        from ..components.Role import Role as role
        from ..components.Actor import Actor as actor
        from ..components.Foundry import Foundry as foundry

        # make a locator
        locator = tracking.simple(f"while resolving '{uri.uri}'")

        # initialize the pile of known candidates
        known = set()

        # the easy things didn't work out; look for matching descriptors
        for candidate in self.retrieveComponentDescriptor(
            uri=uri, protocol=protocol, locator=locator, **kwds
        ):
            # if the candidate is a protocol
            if isinstance(candidate, role):
                # get its default value
                candidate = candidate.pyre_default()
            # if the candidate is a foundry
            if isinstance(candidate, foundry):
                # invoke it
                candidate = candidate()

            # if it is a component class and we have been asked to instantiate it
            if name and isinstance(candidate, actor):
                # build it
                candidate = candidate(name=name, locator=locator)

            # we now have a viable candidate; if it's a known one
            if candidate in known:
                # move on
                continue
            # otherwise, add it to the pile
            known.add(candidate)
            # and hand it to our caller
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
        # grab my name server
        nameserver = self.nameserver
        # get the uri scheme
        scheme = uri.scheme
        # and the address
        address = str(uri.address)
        # if no {scheme} was specified, assume it is {import} and look for possible
        # interpretations of the uri that have been loaded previously
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
                # does the name server recognize it?
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
        yield from self.linker.resolve(
            executive=self, protocol=protocol, uri=uri, **kwds
        )

        # all done
        return

    # registration interface for framework objects
    def registerProtocolClass(self, protocol, family, priority=priority.package):
        """
        Register a freshly minted protocol class
        """
        # make a locator
        pkgloc = tracking.simple(f"while registering protocol '{family}'")
        # get the associated package
        package = self.nameserver.package(executive=self, name=family, locator=pkgloc)
        # associate the protocol with its package
        package.protocols.add(protocol)

        # grab the locator
        locator = protocol.pyre_locator
        # make a priority
        priority = priority()
        # insert the protocol into the model
        key = self.nameserver.configurable(
            name=family, configurable=protocol, priority=priority, locator=locator
        )

        # and return the name server registration key
        return key

    def registerComponentClass(self, component, family, priority=priority.package):
        """
        Register a freshly minted component class
        """
        # make a locator
        pkgloc = tracking.simple(f"while registering component '{family}'")
        # get the associated package
        package = self.nameserver.package(executive=self, name=family, locator=pkgloc)
        # associate the component with its package
        package.components.add(component)

        # grab the locator
        locator = component.pyre_locator
        # make a priority
        priority = priority()
        # insert the component into the model
        key = self.nameserver.configurable(
            name=family, configurable=component, priority=priority, locator=locator
        )
        # return the key
        return key

    def registerComponentInstance(self, instance, name, priority=priority.package):
        """
        Register a freshly minted component instance
        """
        # get the locator
        locator = instance.pyre_locator
        # make a priority
        priority = priority()
        # insert the component instance into the model
        key = self.nameserver.configurable(
            name=name, configurable=instance, priority=priority, locator=locator
        )
        # return the key
        return key

    def registerPackage(self, name, file):
        """
        Register a {pyre} package
        """
        # build a locator
        locator = tracking.here(level=1)
        # get the name server to build one
        package = self.nameserver.createPackage(name=name, locator=locator)
        # register it
        package.register(executive=self, file=primitives.path(file).resolve())
        # configure it
        package.configure(executive=self)

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
        linker = Linker(executive=self, **kwds)
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
        parser.handlers["config"] = self._configurationLoader
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
        # grab my name server
        nameserver = self.nameserver
        # and my file server
        fileserver = self.fileserver

        # access the platform protocol
        from ..platforms import platform

        # get the host class record; the default value already contains all we could discover
        # about the type of machine we are running on
        host = platform().default()
        # set up an iterator over the map of known hosts, in priority order
        knownHosts = nameserver.find(
            pattern=self.hostmapkey, key=operator.attrgetter("priority")
        )
        # go through them
        for info, slot in knownHosts:
            # get the regular expression from the slot value
            regex = slot.value
            # attempt to
            try:
                # compile the regex
                parser = re.compile(regex)
            # if anything goes wrong
            except re.error as error:
                # get the journal
                import journal

                # make a channel
                channel = journal.warning("pyre.config")
                # complain
                channel.line(f"{error}")
                channel.line(f" -- while compiling the regex '{regex}'")
                channel.line(f" -- for '{info.name}'")
                channel.line(f" -- in {info.locator}")
                channel.log(f" -- discarding and moving on...")
                # complain
                continue
            # if either my hostname or my fully qualified domain name is a match
            if parser.match(host.hostname) or parser.match(host.fqdn):
                # extract the nickname as the last part of the key name
                host.nickname = nameserver.split(info.name)[-1]
                # we are done
                break
        # if there was no match
        else:
            # make the hostname be the nickname
            host.nickname = host.hostname

        # get the host information
        self.host = host(name="pyre.host")

        # now the user and the terminal
        from ..shells import user, terminal

        # instantiate them and attach them
        self.user = user(name="pyre.user")
        self.terminal = terminal.pyre_default()(name="pyre.terminal")

        # finally, the environment variables
        from .Environ import Environ

        # instantiate and attach
        self.environ = Environ(executive=self)

        # build weak references to the managers of the runtime environment
        self.dashboard.pyre_user = weakref.proxy(self.user)
        self.dashboard.pyre_host = weakref.proxy(self.host)

        # all done
        return self

    def initializeNamespaces(self):
        """
        Create and initialize the default namespace entries
        """
        # initialize my file server
        self.fileserver.initializeNamespace()
        # initialize my configurator
        self.configurator.initializeNamespace()
        # all done
        return self

    def shutdown(self):
        """
        Clean up
        """
        # my error pile is probably full of circular references
        self.errors = []
        # all done
        return self

    # helpers and other details not normally useful to end users
    def _configurationLoader(self, key, value, locator):
        """
        Handler for the {config} command line argument
        """
        # if the value is empty
        if not value:
            # form the name of the command line argument
            name = ".".join(key)
            # grab the journal
            import journal

            # issue a warning
            journal.warning("pyre.framework").log(f"{name}: no uri")
            # and go no further
            return
        # load the configuration
        self.loadConfiguration(
            uri=value, locator=locator, priority=self.priority.command
        )
        # and return
        return


# end of file
