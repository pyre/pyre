# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre.shells
# my parts
from .Spellbook import Spellbook


# constants
MERLIN = "merlin"


class Merlin(pyre.shells.application, family=MERLIN):
    """
    The merlin executive
    """


    # constants
    merlinFolder = "." + MERLIN


    # public data
    project = None # the project specific settings

    # my subcomponents
    spellbook = None # build at construction time


    # interface
    @pyre.export
    def main(self):
        """
        The main entry point for merlin
        """
        self.fileserver.dump()
        print(" ** main: temporarily disabled")
        return
        # extract the non-configurational parts of the command line
        request = tuple(c for p,c,l in self.executive.configurator.commands) 
        # show the default help screen if there was nothing useful on the command line
        if request == (): 
            import merlin
            return merlin.usage()

        # interpret the request as the name of one of my actors, followed by an argument tuple
        # for the actor's main entry point
        componentName = request[0]
        args = request[1:]

        # convert the component name into a uri
        uri = "import://merlin#{}".format(componentName)

        # attempt to retrieve the component factory
        try:
            factory = self.executive.retrieveComponentDescriptor(uri)
        except self.executive.FrameworkError:
            import merlin
            # NYI: try other component sources
            return merlin.usage()

        # instantiate the component
        actor = factory(name=MERLIN+"-"+componentName)

        # if it is a merlin actor
        if isinstance(actor, pyre.component):
            # ask it to process the user request
            actor.exec(*args)

        # all done
        return self


    @pyre.export
    def help(self, *topics):
        """
        Access to the help system
        """
        print("help:", topics)
        return


    # meta methods
    def __init__(self, name=MERLIN, **kwds):
        super().__init__(name=name, **kwds)

        # hunt down the root of the project where the {.merlin} folder lives
        self.project = self._mountProjectDirectory()
        # create and bind the spell book
        self.spellbook = Spellbook(name=name+".spellbook")

        # all done
        return


    # implementation details
    def _mountProjectDirectory(self):
        """
        Walk up from {cwd} to the directory that contains the {.merlin} folder
        """
        # for path related arithmetic
        import os
        # access the filesystem rooted at the application current directory
        local = self.fileserver['/local']
        # access the filesystem's recognizer
        recognizer = local.recognizer
        # start with the current directory
        curdir = os.path.abspath(local.mountpoint)
        # loop until we find the {.merlin} directory or run up to the root
        while 1:
            # form the candidate path
            candidate = os.path.join(curdir, self.merlinFolder)

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
                # which means that there is no appropriate {.merlin}, so raise an exception
                raise local.NotFoundError(
                    filesystem=local, node=None, path=self.merlinFolder, fragment=self.merlinFolder)
        # got it
        print(" ** project directory at {!r}".format(node.uri))
        # access the filesystem package
        import pyre.filesystem
        # create a local file system
        project = pyre.filesystem.newLocalFilesystem(root=node.uri).discover()
        # build the address
        address = self.fileserver.join(MERLIN, "project")
        # mount it as /merlin/project
        self.fileserver[address] = project
        # and return it
        return project


# end of file 
