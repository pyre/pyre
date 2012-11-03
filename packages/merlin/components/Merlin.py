# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre


class Merlin(pyre.application, family='merlin.application'):
    """
    The merlin executive
    """

    # types
    # exceptions
    from .exceptions import MerlinError

    # public data
    searchpath = pyre.properties.list(
        schema=pyre.schema.str,
        default=['/merlin/project', '/merlin/user', '/merlin/system'])


    # my subcomponents; built at construction time
    user = None # information about the current user
    host = None # information about the host we are running on
    curator = None # the manager of the project persistent store
    spellbook = None # the manager of the installed spells
    packages = None # the package manager

    # public data
    @property
    def metafolder(self):
        return '.' + self.pyre_prefix


    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point for merlin
        """
        # get the commands from the configurator
        commands = self.executive.configurator.commands
        # show the default help screen if there was nothing useful on the command line
        if not commands: return self.help()

        # otherwise, the spell info is in the first entry
        spell = commands[0]
        # and the rest are the arguments to the main entry point of the spell
        args = tuple(command.command for command in commands[1:])
        
        # cast the spell and return its exit status
        return self.cast(name=spell.command, locator=spell.locator, args=args)


    @pyre.export
    def help(self, *topics):
        """
        Access to the help system
        """
        # if not topics were specified
        if not topics:
            # show the default usage message
            from .. import usage
            usage()
            return self
        # otherwise, invoke the help system
        print("help:", topics)
        return self


    # interface
    def cast(self, name, locator, args=()):
        """
        Retrieve a spell by the given {name} and cast it
        """
        # try to
        try:
            # locate the spell
            spell = self.spellbook.findSpell(name=name, locator=locator)
        # if that failed
        except self.FrameworkError:
            # complain
            import journal
            msg = "spell {!r} not found".format(name)
            return journal.error('merlin').log(msg)

        # otherwise, cast it
        return spell.main(*args)


    # support
    def locateProjectRoot(self, folder=None):
        """
        Check whether {folder} is contained within a {merlin} project
        """
        # access to the path utilities
        import os
        # default to checking starting with the current directory
        folder = os.path.abspath(folder) if folder else os.getcwd()
        # loop until we reach the root of the filesystem
        while folder != os.path.sep:
            # form the path to the {.merlin} subdirectory
            metadir = os.path.join(folder, self.metafolder)
            # if it exists
            if os.path.isdir(metadir):
                # got it
                return folder, metadir
            # otherwise, split the path and try again
            folder, _ = os.path.split(folder)
        # if the loop exited normally, we ran up to the root without success; return
        # empty-handed
        return None, None


    # schema factories
    def newProject(self, name):
        """
        Create a new project description object
        """
        # access the class
        from ..schema.Project import Project
        # build the object
        project = Project(name=name)
        # and return it 
        return project
        

    # application initialization hooks
    def pyre_mountVirtualFilesystem(self, root):
        """
        Mount the project directories by walking up from {cwd} to the directory that contains
        the {.merlin} folder
        """
        # chain up to initialize my private area
        pfs = super().pyre_mountVirtualFilesystem(root=root)

        # check whether the project folder is already mounted
        try:
            # by looking for it within my private file space
            pfs['project']
        # if it's not there
        except pfs.NotFoundError:
            # no worries; we'll go hunting
            pass
        # otherwise, it is already mounted; bug?
        else:
            # DEBUG: remove this when happy it never gets called
            raise NotImplementedError('NYI: multiple attempts to initialize the merlin vfs')

        # check whether we are within a project
        root, metadir = self.locateProjectRoot()

        # get the file server
        vfs  = self.vfs
        # build the project folder
        project = vfs.local(root=root).discover() if root else vfs.folder()
        # build the folder with the merlin metadata
        metadata = vfs.local(root=metadir).discover() if metadir else vfs.folder()

        # mount them
        vfs['project'] = project
        pfs['project'] = metadata

        # and return
        return pfs


    # meta methods
    def __init__(self, name, **kwds):
        super().__init__(name=name, **kwds)

        # the host
        from .Host import Host
        self.host = Host(name=name+'.host')
        # the user
        from .User import User
        self.user = User(name=name+'.user')
        # the package manager
        from .PackageManager import PackageManager
        self.packages = PackageManager(name=name+'.packages')
        # the spell book
        from .Spellbook import Spellbook
        self.spellbook = Spellbook(name=name+".spellbook")
        # the curator
        from .Curator import Curator
        self.curator = Curator(name=name+".curator")

        # the asset classifiers
        from .PythonClassifier import PythonClassifier
        self.assetClassifiers = [
            PythonClassifier(name=name+'.python')
            ]

        # all done
        return


# end of file 
