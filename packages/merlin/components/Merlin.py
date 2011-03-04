# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import re

# access to the framework
import pyre


# my metaclass
from pyre.patterns.Singleton import Singleton


class Merlin(metaclass=Singleton):
    """
    The merlin executive
    """


    # constants
    merlinFolder = ".merlin"


    # public data
    system = None # the location of the default configuration
    user = None # the user overrides and extensions
    project = None # the project specific settings

    # access to the pyre executive and its services
    executive = pyre.executive # access to the pyre executive
    fileserver = executive.fileserver # access to the pyre file server

    # properties
    @property
    def spellpath(self):
        return self._spellpath

    @spellpath.setter
    def spellpath(self, folders):
        self._spellpath = folders
        self._spelldirs = re.compile('(' + "|".join(folders) + ')/')
        return


    # interface
    def main(self):
        """
        The main entry point for merlin
        """
        # print(" ** main: temporarily disabled")
        # return
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
        actor = factory(name="merlin-"+componentName)

        # if it is a merlin actor
        if isinstance(actor, pyre.component):
            # ask it to process the user request
            actor.exec(*args)

        # all done
        return self


    def help(self, *topics):
        """
        Access to the help system
        """
        print("help:", topics)
        return


    # utilities
    def findSpells(self, pattern=None):
        # check whether the pattern starts with the name of one of the spell directories look
        # only there
        match = self._spelldirs.match(pattern) if pattern else None
        # if it does
        if match:
            # focus the search on the folder only
            folders = [ match.group(1) ]
            pattern = pattern[match.end():]
        # otherwise
        else:
            folders = self.spellpath
        # iterate through the spell locations
        for folder in folders:
            # look for spells
            for node, path in self.spells[folder].find(pattern=pattern):
                print(node.info.uri)
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # look through the standard configuration folders
        self.system, self.user = self._discoverConfigurationLayout()
        # hunt down the root of the project where the {.merlin} folder lives
        self.project = self._mountProjectDirectory()
        # assemble the spells in their own namespace
        self.spells = self._collectSpells()

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
                    filesystem=local, node=None, path=".merlin", fragment='file')
        # got it
        # access the filesystem package
        import pyre.filesystem
        # create a local file system
        project = pyre.filesystem.newLocalFilesystem(root=node.uri).discover()
        # mount it as /project
        self.fileserver['/project'] = project
        # and return it
        return project


    def _collectSpells(self):
        """
        Traverse the application namespace looking for spells and cataloging them
        """
        # establish the folder
        spells = self.fileserver.newFolder()
        # mount it at the right spot
        self.fileserver['/merlin/spells'] = spells

        # look for the system spell directory
        try:
            # if all is well, this should succeed
            system = self.fileserver['/pyre/system/merlin/spells']
        except self.fileserver.NotFoundError as error:
            # something is wrong with the installation...
            system = self.fileserver.newFolder()
        # attach the system folder
        spells['system'] = system

        # now look for the user's spells
        try:
            # if the user has any spells
            user = self.fileserver['/pyre/user/merlin/spells']
        except self.fileserver.NotFoundError as error:
            # otherwise just build an empty folder
            user = self.fileserver.newFolder()
        # attach the user folder
        spells['user'] = user

        # finally, the project spells
        try:
            # does the project specify any spells?
            project = self.fileserver['/project/spells']
        except self.fileserver.NotFoundError as error:
            # something is wrong with the installation...
            project = self.fileserver.newFolder()
        # attach the project folder
        spells['project'] = project

        # and return it
        return spells


    def _discoverConfigurationLayout(self):
        """
        Look through the standard configuration folders for merlin settings
        """
        # look for the system directory
        try:
            # it should always be there
            system = self.fileserver['/pyre/system/merlin']
        # if not
        except self.fileserver.NotFoundError as error:
            # just create an empty folder
            system = self.fileserver.newFolder()
            # and mount it at the right place
            self.fileserver['pyre/system/merlin'] = system
        # and
        else:
            # fill the folder with its contents
            system.discover()

        # now the user directory
        # if the user has any settings
        try:
            # attach them to our namespace
            user = self.fileserver['/pyre/user/merlin']
        # if not
        except self.fileserver.NotFoundError as error:
            # just create an empty folder
            user = self.fileserver.newFolder()
            # and mount it at the right place
            self.fileserver['pyre/user/merlin'] = user
        # and
        else:
            # fill the folder with its contents
            user.discover()
        # all done
        return system, user


    # private data
    _spellpath = ('project', 'user', 'system')
    _spelldirs = re.compile('(' + "|".join(_spellpath) + ')/')

# end of file 
