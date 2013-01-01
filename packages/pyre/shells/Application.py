# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to the framework
import pyre
# my metaclass
from .Director import Director
# access to the local interfaces
from .Shell import Shell
from .Renderer import Renderer


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
    prefix = None

    # public state
    shell = Shell() # the hosting protocol
    renderer = Renderer() # my custom journal device renderer

    # per-instance public data
    pfs = None # the root of my private filesystem

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
        return self.pyre_executive.fileserver


    @property
    def nameserver(self):
        """
        Easy access to the executive name server
        """
        return self.pyre_executive.nameserver


    # convenience interface
    def error(self, message):
        """
        Generate an error message
        """
        # get the logging mechanism
        import journal
        # build an error message object in my namespace
        error = journal.error(self.pyre_name)
        # log and return
        return error.log(message)
        

    def warning(self, message):
        """
        Generate a warning
        """
        # get the logging mechanism
        import journal
        # build a warning message object in my namespace
        warning = journal.warning(self.pyre_name)
        # log and return
        return warning.log(message)
        

    def info(self, message):
        """
        Generate an informational message
        """
        # get the logging mechanism
        import journal
        # build an informational message object in my namespace
        info = journal.info(self.pyre_name)
        # log and return
        return info.log(message)
        

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
        super().__init__(name=name, **kwds)

        # build my private file space
        self.pfs = self.pyre_mountVirtualFilesystem(root=self.pyre_prefix)

        # attach my renderer to the console
        import journal
        journal.console.renderer = self.renderer

        # all done
        return


    # implementation details
    def run(self, *args, **kwds):
        """
        Ask my shell to launch me
        """
        # easy enough
        return self.shell.launch(application=self, *args, **kwds)


    # initialization hooks
    def pyre_mountVirtualFilesystem(self, root):
        """
        Gather all standard directories that are relevant for this application into its own
        private namespace and register it with the executive file server
        """
        # build the top level folder for my stuff
        pfs = self.vfs.folder()
        # mount it at the right place
        self.vfs[root] = pfs

        # mount the system folder
        folder = 'system'
        pfs[folder] = self.pyre_findFolder(folder=folder, tag=root)
        
        # mount the user folder
        folder = 'user'
        pfs[folder] = self.pyre_findFolder(folder=folder, tag=root)
        
        # and return my private folder
        return pfs


    def pyre_findFolder(self, folder, tag):
        """
        Look through the standard configuration folders for {folder}/{tag}; if the folder does
        not exist, create and mount an empty one.

        The variable {folder} is typically either "system" or "user", although additional
        folders may be explored by default in a future release.

        Mounting an empty folder is a consistency guarantee: applications can access the folder
        and retrieve its contents without first having to test for its existence
        """
        # cache the file server
        fileserver = self.vfs
        # build the target name
        path = fileserver.join("/pyre", folder, tag)
        # look for it 
        try:
            target = fileserver[path]
        # if not there
        except fileserver.NotFoundError:
            # create an empty folder
            target = fileserver.folder()
        # if it is there
        else:
            # fill it up with its contents
            target.discover()
        # and return it
        return target


# end of file 
