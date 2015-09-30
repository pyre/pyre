# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
import sys
# access to the framework
import pyre
# my metaclass
from .Director import Director
# access to the local interfaces
from .Shell import Shell
from .Renderer import Renderer
# so i can describe my dependencies
from .. import externals


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
    DEFAULTS = 'defaults' # the name of the folder with my configuration files

    # the default name for pyre applications; subclasses are expected to provide a more
    # reasonable value, which gets used to load per-instance configuration right before the
    # application itself is instantiated
    pyre_namespace = None

    # public state
    shell = Shell()
    shell.doc = 'my hosting strategy'

    requirements = externals.requirements()
    requirements.doc = 'the list of package categories on which I depend'

    dependencies = externals.dependencies()
    dependencies.doc = 'the map of requirements to package instances that satisfy them'

    interactive = pyre.properties.bool(default=False)
    interactive.doc = "go interactive when no command line arguments are provided"

    DEBUG = pyre.properties.bool(default=False)
    DEBUG.doc = 'debugging mode'

    # per-instance public data
    # geography
    home = None # the directory where my invocation script lives
    prefix = None # my installation directory
    defaults = None # the directory with my configuration folders
    pfs = None # the root of my private filesystem
    layout = None # my configuration options
    renderer = Renderer()

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


    # component interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point of an application component
        """
        # go interactive
        return self.pyre_interactiveSession()


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
        # tell the user what they typed
        self.info.line('{.pyre_namespace}'.format(self))

        # build the simple description of what i do
        for line in self.pyre_help():
            # and push it to my info channel
            self.info.line(line)

        # flush
        self.info.log()
        # and indicate success
        return 0


    # meta methods
    def __init__(self, name=None, **kwds):
        # chain up
        super().__init__(name=name, **kwds)

        # attach my renderer to the console
        import journal
        journal.console.renderer = self.renderer

        # make a name for my channels
        channel  = self.pyre_namespace or name
        # if I have a name
        if channel:
            # build my channels
            self.debug = journal.debug(channel)
            self.firewall = journal.firewall(channel)
            self.info = journal.info(channel).activate()
            self.warning = journal.warning(channel).activate()
            self.error = journal.error(channel).activate()

        # sniff around for my environment
        self.home, self.prefix, self.defaults = self.pyre_explore()
        # instantiate my layout
        self.layout = self.pyre_loadLayout()
        # mount my folders
        self.pfs = self.pyre_makePrivateFilespace()
        # go through my requirements and build my dependency map
        self.dependencies = self.pyre_resolveDependencies()

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
        return Layout()


    def pyre_explore(self):
        """
        Look around my runtime environment and the filesystem for my special folders
        """
        # by default, i have nothing
        home = prefix = defaults = None

        # check how the runtime was invoked
        argv0 = sys.argv[0] # this is guaranteed to exist, but may be empty
        # if it's not empty
        if argv0:
            # turn into an absolute path
            argv0 = os.path.abspath(argv0)
            # if it is a valid file
            if os.path.exists(argv0):
                # split the folder name and save it; that's where i am from...
                home = os.path.dirname(argv0)

        # get my namespace
        namespace = self.pyre_namespace
        # if i have my own home and my own namespace
        if home and namespace:
            # my configuration directory should be at {home}/../defaults/{namespace}
            cfg = os.path.join(home, os.path.pardir, self.DEFAULTS, namespace)
            # if this exists
            if os.path.isdir(cfg):
                # form my prefix
                prefix = os.path.abspath(os.path.join(home, os.path.pardir))
                # and normalize my configuration directory
                defaults = os.path.abspath(cfg)
                # all done
                return home, prefix, defaults

        # let's try to work with my package and my namespace
        package = self.pyre_package()
        # if they both exist
        if package and namespace:
            # get the package prefix
            prefix = package.prefix
            # if it exists
            if prefix:
                # my configuration directory should be at {prefix}/defaults/{namespace}
                cfg = os.path.join(prefix, package.DEFAULTS, namespace)
                # if this exists
                if os.path.isdir(cfg):
                    # and normalize my configuration directory
                    defaults = os.path.abspath(cfg)
                    # all done
                    return home, prefix, defaults

        # all done
        return home, prefix, defaults


    def pyre_makePrivateFilespace(self):
        """
        Build the private filesystem
        """
        # get the file server
        vfs = self.pyre_fileserver
        # get the namespace
        namespace = self.pyre_namespace
        # if i don't have a namespace
        if not namespace:
            # make an empty virtual filesystem and return it
            return vfs.virtual()

        # get/create the top level of my private namespace
        pfs = vfs.getFolder(namespace)

        # check whether
        try:
            # the user directory is already mounted
            pfs[self.USER]
        # if not
        except pfs.NotFoundError:
            # make it
            pfs[self.USER] = vfs.getFolder(vfs.USER_DIR, namespace)

        # get my prefix
        prefix = self.prefix
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
            cfgdir = prefix['defaults/{}'.format(namespace)]
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

        # check whether the parent folder exists
        try:
            # if so, get it
            parent = prefix[folder]
        # if not
        except prefix.NotFoundError:
            # create it
            parent = prefix.mkdir(parent=prefix, name=folder)
        # now, check whether there is a subdirectory named after me
        try:
            # if so get it
            mine = parent[namespace]
        # if not
        except prefix.NotFoundError as error:
            # create it
            mine = prefix.mkdir(parent=parent, name=namespace)

        # attach it to my private filespace
        pfs[folder] = mine

        # all done
        return


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
            package = self.pyre_externals.locate(category=category)
            # store the instance
            dependencies[category] = package

        # all done
        return dependencies


    def pyre_interactiveSession(self):
        """
        Convert this session to an interactive one
        """
        # try to
        try:
            # get readline
            import readline
        # if not there
        except ImportError:
            # no problem
            pass
        # if successful
        else:
            # turn on completion
            import rlcompleter
            # check which interface is available and do the right thing: on OSX, readline is
            # provided by libedit
            if 'libedit' in readline.__doc__:
                # enable completion
                readline.parse_and_bind('bind -v')
                readline.parse_and_bind('bind ^I rl_complete')
            # on other machines, or if the python readline extension is available on OSX
            else:
                # enable completion
                readline.parse_and_bind('tab: complete')

            # attempt to make it possible to save the command history across sessions; we need
            # a name for the history file; check whether I belong to a package
            package = self.pyre_package()
            # in which case
            if package:
                # use its name
                name = package.name
            # otherwise
            else:
                # use 'pyre' by default
                name = 'pyre'

            # get {os.path}
            import os
            # build the uri to the history file
            history = os.path.join(os.path.expanduser('~'), '.{}-history'.format(name))
            # attempt to
            try:
                # read it
                readline.read_history_file(history)
            # if not there
            except IOError:
                # no problem
                pass
            # make sure it gets saved
            import atexit
            # by registering a handler for when the session terminates
            atexit.register(readline.write_history_file, history)

        # go live
        import code, sys
        # adjust the prompts
        sys.ps1 = '{}: '.format(self.pyre_name)
        sys.ps2 = '  ... '
        # adjust the local namespace
        context = self.pyre_interactiveSessionContext()
        # enter interactive mode
        code.interact(banner=self.pyre_banner(), local=context)

        # when the user terminates the session, all done
        return 0


    def pyre_interactiveSessionContext(self):
        """
        Prepare the interactive context by granting access to application parts
        """
        # just me, by default
        return {'self': self}


    def pyre_banner(self):
        """
        Print an identifying message
        """
        return 'entering interactive mode'


    def pyre_fullfillRequest(self, server, request):
        """
        Fulfill a request from an HTTP {server}
        """
        # print the top line
        self.debug.line()
        self.debug.line("server: {}".format(server))
        self.debug.line("  app: {.application}".format(server))
        self.debug.line("  nexus: {.application.nexus}".format(server))
        self.debug.line("request:")
        self.debug.line("  type: {.command!r}".format(request))
        self.debug.line("  path: {.url!r}".format(request))
        self.debug.line("  version: {.version!r}".format(request))
        # print the headers
        self.debug.line("headers:")
        for key, value in request.headers.items():
            self.debug.line(" -- {!r}:{!r}".format(key, value))
        self.debug.log()

        # build a default response
        response = server.responses.OK(
            server=server,
            description="{.pyre_name} does not support web deployment".format(self))
        # and return it
        return response


# end of file
