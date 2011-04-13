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
        # access the file server
        fileserver = self.pyre_executive.fileserver
        # ask for the project pickle file
        db = fileserver["/merlin/project/project.pickle"].open(mode="rb")
        # retrieve the project information
        project  = pickle.load(db)
        # and return it
        return project


    def saveProject(self, project):
        """
        Save the given project configuration to the archive
        """
        # access the file server
        fileserver = self.pyre_executive.fileserver
        # verify that the project directory exists and is mounted
        # if not there, this will raise an exception that the caller has to handle
        folder = fileserver["/merlin/project"]
        # look for the project file and open it in write-binary mode
        try:
            db = folder["project.pickle"].open(mode="wb")
        # if not there, create it
        except folder.NotFoundError:
            # build the path to the file
            path = folder.join(folder.mountpoint, "project.pickle")
            # and open it in write-binary mode
            db = open(path, mode="wb")

        # store the project information
        pickle.dump(project, db)
            
        # and return
        return self


# end of file 
