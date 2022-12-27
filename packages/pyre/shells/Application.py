# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import sys
# access to the framework
import pyre
import journal
# my metaclass
from .Director import Director
# protocols
from .Shell import Shell


# declaration
class Application(pyre.component, metaclass=Director):
    """
    Abstract base class for top-level application components

    {Application} streamlines the interaction with the pyre framework. It is responsible for
    staging an application process, i.e. establishing the process namespace and virtual
    filesystem, configuring the help system, and supplying the main behavior.
    """


    # constants
    USER = 'user' # the name of the folder with user settings
    SYSTEM = 'system' # the name of the folder with the global settings
    CONFIG = 'share' # the name of the folder with my configuration files

    # the default name for pyre applications; subclasses are expected to provide a more
    # reasonable value, which gets used to load per-instance configuration right before the
    # application itself is instantiated
    pyre_namespace = None

    # public state
    shell = Shell()
    shell.doc = 'my hosting strategy'

    DEBUG = pyre.properties.bool(default=False)
    DEBUG.doc = 'debugging mode'

    # per-instance public data
    # geography
    pyre_home = None # the directory where my invocation script lives
    pyre_prefix = None # my installation directory
    pyre_config = None # the directory with my configuration folders
    pfs = None # the root of my private filesystem
    layout = None # my configuration options

    # journal channels
    info = None
    warning = None
    error = None
    debug = None
    firewall = None

    # public data
    # properties
    @property
    def executive(self):
        """
        Provide access to the pyre executive
        """
        return self.pyre_executive

    @property
    def vfs(self):
        """
        Easy access to the executive file server
        """
        return self.pyre_fileserver

    @property
    def nameserver(self):
        """
        Easy access to the executive name server
        """
        return self.pyre_nameserver


    @property
    def argv(self):
        """
        Return an iterable over the command line arguments that were not configuration options
        """
        # the {configurator} has what I am looking for
        for command in self.pyre_configurator.commands:
            # but it is buried
            yield command.command
        # all done
        return


    @property
    def searchpath(self):
        """
        Build a list of unique package names from my ancestry in mro order
        """
        # path
        path = set()
        # go through all my ancestors
        for base in self.pyre_public():
            # get the package name
            name = base.pyre_package().name
            # if the name has not been seen before
            if name not in path:
                # send it to the caller
                yield name
                # add it
                path.add(name)
        # all done
        return


    # component interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point of an application component
        """
        # the default behavior is to show the help screen
        return self.help(**kwds)


    @pyre.export
    def launched(self, *args, **kwds):
        """
        Notification issued by some shells that application launching is complete
        """
        # nothing to do but indicate success
        return 0


    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        # make a channel
        channel = journal.help("pyre.help.application")
        # build the simple description of what i do and render it
        channel.report(report=self.pyre_help())
        # flush
        channel.log()
        # and indicate success
        return 0


    # meta methods
    def __init__(self, name=None, **kwds):
        # chain up
        super().__init__(name=name, **kwds)

        # get the executive
        executive = self.pyre_executive
        # set up my nickname
        nickname = self.pyre_namespace or name

        # get the dashboard
        dashboard = executive.dashboard
        # check whether there is already an app registered with the dashboard
        if dashboard.pyre_application is not None:
            # make a channel
            channel = journal.warning(f"{nickname}")
            # complain
            channel.line(f"while registering {self}:")
            channel.line(f"another app, {dashboard.pyre_application}, is already registered")
            channel.log()
        # in any case, attach me to the dashboard
        dashboard.pyre_application = self

        # if i have one
        if nickname:
            # register it with the journal
            journal.application(name=nickname)

            # build my channels
            self.debug = journal.debug(nickname)
            self.firewall = journal.firewall(nickname)
            self.info = journal.info(nickname).activate()
            self.warning = journal.warning(nickname).activate()
            self.error = journal.error(nickname).activate()
            # if i am in debugging mode
            if self.DEBUG:
                # activate the debug channel
                self.debug.active = True

        # sniff around for my environment
        self.pyre_home, self.pyre_prefix, self.pyre_config = self.pyre_explore()
        # instantiate my layout
        self.layout = self.pyre_loadLayout()
        # mount my folders
        self.pfs = self.pyre_mountPrivateFilespace()

        # if i have a name
        if name is not None:
            # build a locator
            loc = pyre.tracking.simple(f"while initializing application '{nickname}'")
            # load my configuration files
            self.pyre_loadConfiguration(locator=loc)

        # go through my requirements and build my dependency map
        # self.dependencies = self.pyre_resolveDependencies()

        # all done
        return


    # implementation details
    def run(self, *args, **kwds):
        """
        Ask my shell to launch me
        """
        # easy enough
        return self.shell.launch(self, *args, **kwds)


    # initialization hooks
    def pyre_loadLayout(self):
        """
        Create my application layout object, typically a subclass of {pyre.shells.Layout}
        """
        # access the factory
        from .Layout import Layout
        # build one and return it
        return Layout(name=f"{self.pyre_name}.layout")


    def pyre_loadConfiguration(self, locator):
        """
        Load my configuration files
        """
        # get my name
        name = self.pyre_name
        # and the executive
        executive = self.pyre_executive
        # ask it to hunt down configuration files derived from my name
        executive.configure(namespace=name, locator=locator)
        # all done
        return


    def pyre_explore(self):
        """
        Look around my runtime environment and the filesystem for my special folders
        """
        # by default, i have nothing
        home = prefix = config = None

        # check how the runtime was invoked
        argv0 = sys.argv[0] # this is guaranteed to exist, but may be empty
        # if it's not empty, i was instantiated from within a script; hopefully, one of mine
        if argv0:
            # turn into an absolute path
            argv0 = pyre.primitives.path(argv0).resolve()
            # if it is a valid file
            if argv0.exists():
                # split the folder name and save it; that's where i am from...
                home = argv0.parent
                # and my prefix is its parent folder
                prefix =  home.parent

        # at this point, i either have both {home} and {prefix}, or neither; there isn't much more
        # to be done about {home}, but i still have a shot to find the system {config} by
        # examining my {package}
        package = self.pyre_package()
        # if i don't know my {prefix} and my package has one
        if prefix is None and package.prefix:
            # use it; it's almost certainly a better choice that leaving it empty
            prefix = package.prefix

        # finding my {config} directory requires me to have a namespace
        namespace = self.pyre_namespace

        # if i don't have both
        if not prefix or not namespace:
            # not much more to do
            return home, prefix, config

        # look for my configuration directory
        cfg = prefix / self.CONFIG / namespace
        # if it exists
        if cfg.isDirectory():
            # all done
            return home, prefix, cfg

        # otherwise, not much else to do
        return home, prefix, config


    def pyre_mountPrivateFilespace(self):
        """
        Build the private filesystem
        """
        # get the file server
        vfs = self.vfs
        # get the namespace
        namespace = self.pyre_namespace
        # if i don't have a namespace
        if not namespace:
            # make an empty virtual filesystem and return it
            return vfs.virtual()

        # attempt to
        try:
            # get my private filespace
            pfs = vfs[namespace]
        # if not there
        except vfs.NotFoundError:
            # make it
            pfs = vfs.folder()
            # and mount it
            vfs[namespace] = pfs

        # check whether
        try:
            # the user directory is already mounted
            pfs[self.USER]
        # if not
        except pfs.NotFoundError:
            # check whether
            try:
                # i have a folder in the user area
                userdir = vfs[vfs.USER_DIR, namespace]
            # if not
            except vfs.NotFoundError:
                # make and mount an empty folder
                pfs[self.USER] = pfs.folder()
            # if it is there
            else:
                # look deeply
                userdir.discover()
                # and mount it
                pfs[self.USER] = userdir

        # get my prefix
        prefix = self.pyre_prefix
        # if i don't have one
        if not prefix:
            # attach an empty folder; must use {pfs} to do this to guarantee filesystem consistency
            pfs[self.SYSTEM] = pfs.folder()
            # and return
            return pfs
        # otherwise, get the associated filesystem
        home = vfs.retrieveFilesystem(root=prefix)
        # and mount my folders in my namespace
        self.pyre_mountApplicationFolders(pfs=pfs, prefix=home)

        # now, build the protocol resolution folders by assembling the contents of the
        # configuration folders in priority order
        for root in [self.SYSTEM, self.USER]:
            # build the work list: triplets of {name}, {source}, {destination}
            todo = [ (root, pfs[root], pfs) ]
            # now, for each triplet in the work list
            for path, source, destination in todo:
                # go through all the children of {source}
                for name, node in source.contents.items():
                    # if the node is a folder
                    if node.isFolder:
                        # gingerly attempt to
                        try:
                            # grab the associated folder in {destination}
                            link = destination[name]
                        # if not there
                        except destination.NotFoundError:
                            # no worries, make it
                            link = destination.folder()
                            # and attach it
                            destination[name] = link
                        # add it to the work list
                        todo.append( (name, node, link) )
                    # otherwise
                    else:
                        # link the file into the destination folder
                        destination[name] = node

        # all done
        return pfs


    def pyre_mountApplicationFolders(self, pfs, prefix):
        """
        Explore the application installation folders and construct my private filespace
        """
        # get my namespace
        namespace = self.pyre_namespace
        # look for
        try:
            # the folder with my configurations
            cfgdir = prefix[f"{self.CONFIG}/{namespace}"]
        # if it is not there
        except pfs.NotFoundError:
            # make an empty folder; must use {pfs} to do this to guarantee filesystem consistency
            cfgdir = pfs.folder()
        # attach it
        pfs[self.SYSTEM] = cfgdir

        # now, my runtime folders
        folders = [ 'etc', 'var' ]
        # go through them
        for folder in folders:
            # and mount each one
            self.pyre_mountPrivateFolder(pfs=pfs, prefix=prefix, folder=folder)

        # all done
        return pfs


    def pyre_mountPrivateFolder(self, pfs, prefix, folder):
        """
        Look in {prefix} for {folder}, create it if necessary, and mount it within {pfs}, my
        private filespace
        """
        # get my namespace
        namespace = self.pyre_namespace
        # sign in
        # print(f"Application.pyre_mountPrivateFolder:")
        # print(f"  looking for: {prefix.uri}/{folder}/{namespace}")
        # give me the context

        # check whether the parent folder exists
        try:
            # if so, get it
            parent = prefix[folder]
        # if not
        except prefix.NotFoundError:
            # attempt to
            try:
                # create it
                parent = prefix.mkdir(name=folder)
            # if something goes wrong
            except OSError:
                # bail
                return
        # the directory is there; look for content
        parent.discover(levels=1)
        # now, check whether there is a subdirectory named after me
        try:
            # if so get it
            mine = parent[namespace]
        # if not
        except prefix.NotFoundError as error:
            # attempt to
            try:
                # create it
                mine = parent.mkdir(name=namespace)
            # if something goes wrong
            except OSError:
                # bail
                return
            # and show me
            # print(f"  created {mine.uri}")
        # if all went well
        else:
            # show me
            # print(f"  mounted {mine.uri}")
            # look carefully; there may be large subdirectories beneath
            mine.discover(levels=1)

        # attach it to my private filespace
        pfs[folder] = mine

        # all done
        return


    def pyre_locateParentWith(self, marker, folder=None):
        """
        Locate the directory that contains {marker}, starting with {folder} of the {cwd} and
        moving upwards
        """
        # if the caller has not expressed an opinion start with the current working directory
        folder = pyre.primitives.path.cwd() if folder is None else folder
        # go through folders on the way to the root of the filesystem
        for candidate in folder.crumbs:
            # form the filename
            target = candidate / marker
            # if it exists
            if target.exists():
                # we are done
                return candidate
        # if we get this far, the marker could not be fund
        return None


    def pyre_resolveDependencies(self):
        """
        Go through my list of required package categories and resolve them

        The result is a map from package categories to package instances that satisfy each
        requirement. This map includes dependencies induced while trying to satisfy my
        requirements
        """
        # initialize the map
        dependencies = {}

        # do the easy thing, for now
        for category in self.requirements:
            # ask the external manager for a matching package
            package = self.pyre_host.packager.locate(category=category)
            # store the instance
            dependencies[category] = package

        # all done
        return dependencies


    # other behaviors
    def pyre_shutdown(self, **kwds):
        """
        Release all resources and prepare to exit
        """
        # nothing to do...
        return


    def pyre_interrupted(self, **kwds):
        """
        The user issued a keyboard interrupt
        """
        # show me
        self.warning.log("interrupted; exiting")
        # indicate something went wrong
        return 1


    def pyre_interactiveSessionContext(self, context=None):
        """
        Prepare the interactive context by granting access to application parts
        """
        # prime the execution context
        context = context or {}
        # grant access to pyre
        context['pyre'] = pyre
        # by default, nothing to do: the shell has already bound me in this context
        return context


    def pyre_interactiveBanner(self):
        """
        Print an identifying message for the interactive session
        """
        # just saying hi...
        return 'entering interactive mode...\n'


    # basic support for the help system
    def pyre_help(self, indent=' '*2, **kwds):
        """
        Hook for the application help system
        """
        # make a mark
        yield from self.pyre_banner()
        # my summary
        yield from self.pyre_showSummary(indent=indent, **kwds)
        # usage
        yield ""
        yield "usage:"
        yield f"{indent}{self.pyre_name} [options]"
        yield ""

        # my public state
        yield from self.pyre_showConfigurables(indent=indent, **kwds)
        # all done
        return


    def pyre_banner(self):
        """
        Print an identifying message for the help system
        """
        # easy
        return []


    def pyre_respond(self, server, request):
        """
        Fulfill a request from an HTTP {server}
        """
        # grab my debug channel
        channel = self.debug
        # print the top line
        channel.line(f"responding to HTTP request:")
        channel.line(f"  app: {self}")
        channel.line(f"  nexus: {self.nexus}")
        channel.line(f"  server: {server}")
        # dump the request contents
        request.dump(channel=channel, indent='  ')
        # flush
        channel.log()

        # build a default response
        response = server.responses.NotFound(
            server=server,
            description=f"{self.pyre_name} does not support web deployment")
        # and return it
        return response


# end of file
