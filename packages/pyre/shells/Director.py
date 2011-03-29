# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..components.Actor import Actor


class Director(Actor):
    """
    The metaclass of applications

    {Director} takes care of all the tasks necessary to register an application family with the
    framework
    """

    # meta methods
    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new application class record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)
        # if I am a hidden application subclass, we are all done
        if self.pyre_hidden: return

        # otherwise
        # build the private file space
        self.pyre_filesystem = self._pyre_buildPrivateFilespace()

        # all done
        return


    # implementation details
    def _pyre_buildPrivateFilespace(self):
        """
        Gather all standard directories that are relevant for this application family into its
        own private namespace and register it with the executive file server
        """
        # build the top level folder for my stuff
        private = self.pyre_executive.fileserver.newFolder()
        # flatten my family
        family = self.pyre_SEPARATOR.join(self.pyre_family)
        # mount it at the right place
        self.pyre_executive.fileserver[family] = private
        # mount the system folder
        self._pyre_mountFolder(parent=private, folder="system", tag=family)
        # mount the user folder
        self._pyre_mountFolder(parent=private, folder="user", tag=family)
        # and return the private folder
        return private
        


    def _pyre_mountFolder(self, folder, parent, tag):
        """
        Look through the standard configuration folders for {tag}/{folder} and mount it in the
        application private namespace anchored at {parent}. If the folder does not exist,
        create and mount an empty one.

        The variable {folder} is typically either "system" or "user", although additional
        folders may be explored by default in a future release.

        Mounting an empty folder is a consistency guarantee: applications can access the folder
        and retrieve its contents without having to first test for its existence
        """
        # cache the file server
        fileserver = self.pyre_executive.fileserver
        # build the target name
        path = fileserver.join("/pyre", folder, tag)
        # look for it 
        try:
            target = fileserver[path]
        # if not there
        except fileserver.NotFoundError:
            # create an empty folder
            target = fileserver.newFolder()
        # if it is there
        else:
            # fill it up with its contents
            target.discover()
        # in any case, mount it
        parent[folder] = target
        # and return
        return


# end of file 
