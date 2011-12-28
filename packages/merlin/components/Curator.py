# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre


# other packages
import pickle


# declaration
class Curator(pyre.component, family="merlin.curator"):
    """
    The component that manages the project persistent store
    """


    # interface
    def loadProject(self):
        """
        Retrieve the project configuration information from the archive
        """
        # retrieve the project instance from the file
        return self._load(tag="project")


    def saveProject(self, project):
        """
        Save the given project configuration to the archive
        """
        # pickle the project information into the associated file
        self._save(tag="project", item=project)
        # and return
        return self


    # implementation details
    def _load(self, tag):
        """
        Retrieve an object from the merlin file identified by {tag}
        """
        # access the file server
        fileserver = self.pyre_executive.fileserver
        # derive the filename from {tag}
        vname = "/merlin/project/{}.pickle".format(tag)
        # open the associated file; the caller is responsible for catching any exceptions
        store = fileserver[vname].open(mode="rb")
        # retrieve the object from the store
        item = pickle.load(store)
        # and return it
        return item


    def _save(self, tag, item):
        """
        Pickle {item} into the merlin file indicated by {tag}
        """
        # access the file server
        fileserver = self.pyre_executive.fileserver
        # verify that the project directory exists and is mounted; the caller is responsible
        # for catching any exceptions
        folder = fileserver["/merlin/project"]
        # build the filename associated with {tag}
        vname = "{}.pickle".format(tag)
        # look for the file
        try:
            # careful: this overwrites existing files
            store = folder[vname].open(mode="wb")
        # if not there, create it
        except folder.NotFoundError:
            # FIXME - FILESERVER: this steps outside the file server abstraction, since file
            # creation is not supported yet
            # build the path to the file
            path = folder.join(folder.uri, vname)
            # and open it in write-binary mode
            store = open(path, mode="wb")
        # pickle the item
        pickle.dump(item, store)
        # and return
        return
        


# end of file 
