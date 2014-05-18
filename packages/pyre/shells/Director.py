# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os
import weakref
# framework access
import pyre


# declaration
class Director(pyre.actor):
    """
    The metaclass of applications

    {Director} takes care of all the tasks necessary to register an application family with the
    framework
    """


    # meta methods
    def __init__(self, name, bases, attributes, prefix=None, **kwds):
        """
        Initialization of application class records
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)

        # if i don't have a prefix
        if not prefix:
            # get my package
            package = self.pyre_package()
            # and if it exists
            if package:
                # use its name as my prefix
                prefix = package.name
        # if i now have a prefix
        if prefix:
            # populate and mount the private filesystem; 
            pfs = self.pyre_mountApplicationFolders(prefix)
        # otherwise
        else:
            # make an empty one
            pfs = self.pyre_fileserver.virtual()

        # attach it
        self.pfs = pfs

        # all done
        return


    def __call__(self, name=None, globalAliases=True, locator=None, **kwds):
        """
        Instantiate one of my classes
        """
        # get the executive
        executive = self.pyre_executive
        # if I have a name for the application instance, use it to hunt down configuration
        # files for this particular instance
        if name:
            # set up the priority
            priority = executive.priority.package
            # build a locator
            initloc = pyre.tracking.simple('while initializing application {!r}'.format(name))
            # ask the executive to hunt down the application INSTANCE configuration file
            executive.configure(stem=name, priority=priority, locator=initloc)

        # record the caller's location
        locator = pyre.tracking.here(1) if locator is None else locator
        # chain up to create the instance
        app = super().__call__(name=name, globalAliases=globalAliases, locator=locator, **kwds)
        # attach it to the executive
        executive.application = weakref.proxy(app)
        # and return it
        return app


    # implementation details
    def pyre_mountApplicationFolders(self, prefix):
        """
        Build the private filesystem
        """
        # get the file server
        vfs = self.pyre_fileserver
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
        installdir = os.path.abspath(os.path.join(os.path.pardir, self.home))
        # get the associated filesystem
        home = vfs.retrieveFilesystem(root=installdir)
        # look for
        try:
            # the folder with my configurations
            cfgdir = home['defaults/{}'.format(prefix)]
        # if it is not there
        except vfs.NotFoundError:
            # make an empty folder
            cfgdir = home.folder()
        # attach it
        pfs['system'] = cfgdir

        # all done
        return pfs


# end of file 
