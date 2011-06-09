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


class Merlin(pyre.application, family=MERLIN):
    """
    The merlin executive
    """


    # constants
    merlinFolder = "." + MERLIN


    # types
    from .Curator import Curator
    from .Spellbook import Spellbook
    # exceptions
    from .exceptions import MerlinError


    # my subcomponents; built at construction time
    curator = None # the manager of the project persistent store
    spellbook = None # the manager of the installed spells


    # interface
    @pyre.export
    def main(self):
        """
        The main entry point for merlin
        """
        # extract the non-configurational parts of the command line
        request = tuple(c for _,c,_ in self.executive.configurator.commands) 
        # show the default help screen if there was nothing useful on the command line
        if request == (): 
            return self.help()

        # interpret the request as the name of one of my actors, followed by an argument tuple
        # for the actor's main entry point
        spell = request[0]
        args = request[1:]

        # instantiate the component
        try:
            actor = self.spellbook.findSpell(name=spell)
        except self.FrameworkError:
            print("spell {!r} not found".format(spell))
            return self

        # if it is a merlin actor
        if isinstance(actor, pyre.component):
            # ask it to process the user request
            actor.main(*args)

        # all done
        return self


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
    def pyre_mountApplicationFolders(cls):
        """
        Mount the project directory by walking up from {cwd} to the directory that contains the
        {.merlin} folder
        """
        # access the file server
        fileserver = cls.pyre_executive.fileserver
        # build the address where the project .merlin directory will be mounted
        vpath = fileserver.join(MERLIN, "project")
        # is it already there?
        try:
            folder = fileserver[vpath]
        # if not, go looking for it
        except fileserver.NotFoundError:
            pass
        # otherwise, it is already mounted
        else:
            # print("Merlin.pyre_mountApplicationFolders: already mounted")
            return
        # go file hunting
        # for path related arithmetic
        import os
        # access the filesystem rooted at the application current directory
        local = fileserver['/local']
        # access the filesystem's recognizer
        recognizer = local.recognizer
        # start with the current directory
        curdir = os.path.abspath(local.mountpoint)
        # loop until we find the {.merlin} directory or run up to the root
        while 1:
            # form the candidate path
            candidate = os.path.join(curdir, cls.merlinFolder)

            try:
                # get the file server's recognizer to tell us what this is
                node = recognizer.recognize(candidate)
            except OSError:
                # the file doesn't exist; move on
                pass
            else:
                # if it is a directory, we are done
                if node.isDirectory(): break
            # if we got this far, the current guess for the {.merlin} directory was no good
            # save this path
            olddir = curdir
            # try the parent
            curdir = os.path.abspath(os.path.join(curdir, os.pardir))
            # if the parent directory is identical with the current directory, we are at the root
            if olddir == curdir:
                # which means that there is no appropriate {.merlin}, so return empty-handed
                return
        # got it
        # print(" ** project directory at {!r}".format(node.uri))
        # access the filesystem package
        import pyre.filesystem
        # create a local file system
        project = pyre.filesystem.newLocalFilesystem(root=node.uri).discover()
        # mount it as /merlin/project
        fileserver[vpath] = project
        # and return it
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

        # create and bind the spell book
        self.spellbook = self.Spellbook(name=name+".spellbook")
        # create and bind the curator
        self.curator = self.Curator(name=name+".curator")

        # register the components that explore my vfs looking for configuration choices
        self.categories = {
            "spells": self.spellbook,
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
