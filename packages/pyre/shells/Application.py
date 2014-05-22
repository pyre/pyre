# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
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
    # the default name for pyre applications; subclasses are expected to provide a more
    # reasonable value, which gets used to load per-instance configuration right before the
    # application itself is instantiated
    pyre_prefix = None

    # public state
    shell = Shell()
    shell.doc = 'my hosting strategy'

    renderer = Renderer()
    renderer.doc = 'my custom journal device renderer'

    requirements = externals.requirements()
    requirements.doc = 'the list of package categories on which I depend'

    dependencies = externals.dependencies()
    dependencies.doc = 'the map of requirements to package instances that satisfy them'
    
    # per-instance public data
    pfs = None # the root of my private filesystem
    # journal channels
    info = None
    warning = None
    error = None
    debug = None
    firewall = None

    # public data
    home = os.path.dirname(sys.argv[0])

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
    def main(self, **kwds):
        """
        The main entry point of an application component
        """
        raise NotImplementedError(
            "application {.pyre_name!r} must implement 'main'".format(self))
        

    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        raise NotImplementedError(
            "application {.pyre_name!r} must implement 'help'".format(self))
        

    # meta methods
    def __init__(self, name=None, **kwds):
        # chain up
        super().__init__(name=name, **kwds)

        # mount my folders
        self.pfs = self.pyre_mountApplicationFolders()
        # go through my requirements and build my dependency map
        self.dependencies = self.pyre_resolveDependencies()

        # attach my renderer to the console
        import journal
        journal.console.renderer = self.renderer

        # if I have a name
        if name:
            # build my channels
            self.debug = journal.error(name)
            self.firewall = journal.error(name)
            self.info = journal.info(name).activate()
            self.warning = journal.warning(name).activate()
            self.error = journal.error(name).activate()

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
    def pyre_mountApplicationFolders(self):
        """
        Build the private filesystem
        """
        # get the file server
        vfs = self.pyre_fileserver
        # get the prefix
        prefix = self.pyre_prefix
        # if i don't have a prefix
        if not prefix:
            # make an empty virtual filesystem and return it
            return vfs.virtual()
        # get/create the top level of my private namespace
        pfs = vfs.getFolder(prefix)

        # check whether 
        try:
            # the user directory is already mounted
            pfs['user']
        # if not
        except pfs.NotFoundError:
            # make it
            pfs['user'] = vfs.getFolder(vfs.USER_DIR,  prefix)

        # now, let's hunt down the application specific configurations
        # my installation directory is the parent folder of my home
        installdir = os.path.abspath(os.path.join(self.home, os.path.pardir))
        # get the associated filesystem
        home = vfs.retrieveFilesystem(root=installdir)
        # look for
        try:
            # the folder with my configurations
            cfgdir = home['defaults/{}'.format(prefix)]
        # if it is not there
        except vfs.NotFoundError:
            # make an empty folder; must use {pfs} to do this to guarantee filesystem consistency
            cfgdir = pfs.folder()
        # attach it
        pfs['system'] = cfgdir

        # all done
        return pfs


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


# end of file 
