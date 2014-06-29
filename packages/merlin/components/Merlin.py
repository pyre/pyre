# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os
# access the pyre framework
import pyre
# and my action protocol
from .Spell import Spell as spell


# class declaration; merlin is a plexus app
class Merlin(pyre.plexus, family='merlin.components.plexus', action=spell):
    """
    The merlin executive and application wrapper
    """


    # types
    # exceptions
    from .exceptions import MerlinError, SpellNotFoundError


    # constants
    METAFOLDER = '.merlin'
    PATH = ['vfs:/merlin/project', 'vfs:/merlin/user', 'vfs:/merlin/system']

    # user configurable state
    searchpath = pyre.properties.paths(default=PATH)


    # interface
    @pyre.export
    def help(self, *topics):
        """
        Provide help on {topics}
        """
        # if not topics were specified
        if not topics:
            # get the usage message from the packages
            from .. import usage
            # invoke it
            usage()
            # indicate success
            return 0

        # otherwise, invoke the help system
        print('help:', topics)
        # all done
        return 0


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
        

    # meta methods
    def __init__(self, name, **kwds):
        super().__init__(name=name, **kwds)

        # the spell manager is built during the construction of superclass; local alias
        self.spellbook = self.repertoir

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


    # framework requests
    def pyre_mountApplicationFolders(self, pfs, prefix):
        """
        Build my private filesystem
        """
        # chain up
        pfs = super().pyre_mountApplicationFolders(pfs=pfs, prefix=prefix)

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


    # support
    def newRepertoir(self):
        """
        Build my spell manager
        """
        # access the factory
        from .Spellbook import Spellbook
        # make one and return it
        return Spellbook(protocol=self.pyre_action)


    def locateProjectRoot(self, folder=None):
        """
        Check whether {folder} is contained within a {merlin} project
        """
        # default to checking starting with the current directory
        folder = os.path.abspath(folder) if folder else os.getcwd()
        # loop until we reach the root of the filesystem
        while folder != os.path.sep:
            # form the path to the {.merlin} subdirectory
            metadir = os.path.join(folder, self.METAFOLDER)
            # if it exists
            if os.path.isdir(metadir):
                # got it
                return folder, metadir
            # otherwise, split the path and try again
            folder, _ = os.path.split(folder)
        # if the loop exited normally, we ran up to the root without success; return
        # empty-handed
        return None, None


# end of file 
