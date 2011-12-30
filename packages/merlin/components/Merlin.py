# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre


# constants
MERLIN = "merlin"


class Merlin(pyre.application):
    """
    The merlin executive
    """


    # constants
    merlinFolder = "." + MERLIN


    # types
    # exceptions
    from .exceptions import MerlinError


    # my subcomponents; built at construction time
    user = None # information about the current user
    host = None # information about the host we are running on
    curator = None # the manager of the project persistent store
    spellbook = None # the manager of the installed spells
    packages = None # the package manager


    # interface
    @pyre.export
    def main(self):
        """
        The main entry point for merlin
        """
        # extract the non-configurational parts of the command line
        request = tuple(c for _,c,_ in self.executive.configurator.commands) 
        # show the default help screen if there was nothing useful on the command line
        if request == (): return self.help()

        # interpret the request as the name of one of my actors, followed by an argument tuple
        # for the actor's main entry point
        spell = request[0]
        args = request[1:]

        # and cast it
        return self.cast(name=spell, args=args)


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
    def cast(self, name, args=()):
        """
        Retrieve a spell by the given {name} and cast it
        """
        # try to
        try:
            # locate the spell
            spell = self.spellbook.findSpell(name=name)
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
            metadir = os.path.join(folder, self.merlinFolder)
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
    def pyre_mountApplicationFolders(self):
        """
        Mount the project directories by walking up from {cwd} to the directory that contains
        the {.merlin} folder
        """
        # access the file server
        fileserver = self.pyre_executive.fileserver
        # build the address where the project {.merlin} directory will be mounted
        vpath = fileserver.join(MERLIN, "project")
        # is it already there?
        try:
            folder = fileserver[vpath]
        # if not
        except fileserver.NotFoundError:
            # no worries; we'll go hunting
            pass
        # otherwise, it is already mounted
        else:
            # print("Merlin.pyre_mountApplicationFolders: already mounted")
            return

        # check whether we are within a project
        root, metadir = self.locateProjectRoot()
        # if not, we are done
        if not root: return

        # otherwise
        import pyre.filesystem
        # first, mount the project root as {/project}
        fileserver['/project'] = pyre.filesystem.local(root=root)
        # next, mount the {merlin} meta-data directory as {/merlin/project}
        fileserver[vpath] = pyre.filesystem.local(root=metadir).discover()
        # and return
        return


    # namespace resolver obligations
    # support for automatically resolving merlin names
    def pyre_componentSearchPath(self, context):
        """
        Hook invoked during the resolution of component names into descriptors.

        merlin iterates through the each of the standard places, asking a {context} specific
        sub-component for assistance in retrieving candidate shelves from the filesystem.
        """
        # the first part is my tag
        assert context[0] == MERLIN
        # if there is only one fragment
        if len(context) == 1:
            # there is nothing to do
            return

        # what are we looking for?
        category = context[1]
        # look up the responsible subcomponent
        try:
            component = self.categories[category]
        except KeyError:
            # any other ideas?
            return

        # my file server
        vfs = self.vfs
        # iterate over the standard locations
        for root in self.configpath:
            # form the name of category sub folder
            location = vfs.join(root, category)
            # and look for it
            try:
                folder = vfs[location]
            # if not there
            except vfs.NotFoundError:
                # move on to the next one
                continue
            # hand each one to the resolving subcomponent and get back shelves
            for shelf in component.shelves(folder=folder, name=location):
                # which, in turn, are processed by the caller
                yield shelf

        # no more
        return


    # meta methods
    def __init__(self, name=MERLIN, **kwds):
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

        # register the components that explore my vfs looking for configuration choices
        self.categories = {
            "spells": self.spellbook,
            "packages": self.packages,
            }

        # the ordered list of folders to visit while resolving names
        self.configpath = [
            '/merlin/project',
            '/merlin/user',
            '/merlin/system',
            ]

        # all done
        return


# end of file 
