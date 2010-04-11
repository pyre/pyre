# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
from pyre.filesystem.Filesystem import Filesystem


class FileServer(Filesystem):

    """
    The manager of the virtual filesystem

    Intances of FileServer manage hierarchical namespaces implemented as a virtual
    filesystem. The contents of these namespaces are retrieved using URIs, and can be arbitrary
    objects, although they are typically either local or remote files.

    The framework uses a FileServer instance to decouple the logical names of resources from
    their physical locations at runtime. For example, as part of the bootstrapping process, the
    frameworks discovers the pyre installation directory; the persistent store for the default
    component configurations is a subdirectory of that location and it is mounted as
    '/pyre/system' in the virtual filesystem. This has the following benefits:
    
    * applications can navigate through the contents of '/pyre/system' as if it were an actual
      filesystem

    * configuration settings that require references to entries in '/pyre/system' can now be
      expressed portably, since there is no need to hardwire actual paths

    Similarly, user preferences are retrieved from '/pyre/user', which typically refers to the
    subdirectory '.pyre' of the user's home directory, but may be populated from other sources,
    depending on the operating system.

    Applications are encouraged to lay out their own custom namespaces. The application
    developer can refer to resources through their standardized logical names, whereas the user
    is free to provide the mapping that reflects their physical location at runtime.
    """


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # access the symbols we need
        import pyre
        import pyre.filesystem

        # first, mount the system directory
        # there are two possibilities
        #  - it is an actual location on the disk
        #  - it is inside a zip file
        # the way to tell is by checking whether pyre.prefix() points to an actual directory
        # both are handled correctly by the pyre.filesystem.newFilesystem factory
        try:
            # so invoke it to build the filesystem for us
            self.systemfs = pyre.filesystem.newFilesystem(pyre.prefix())
        except pyre.filesystem.GenericError:
            # if this failed, just create a new empty folder
            system = self.newFolder()
        else:
            try:
                # hunt down the depository subdirectory
                system = self.systemfs["depository"]
            except KeyError:
                # hmm... why is this directory missing from the distribution?
                # moving on...
                system = self.newFolder()
       # mount the system directory
        self["pyre/system"] = system

        # now, mount the user's home directory
        # the default location of user preferences is in ~/.pyre
        try:
            # make filesystem out of the preference directory
            self.userfs = pyre.filesystem.newFilesystem(os.path.expanduser(self.DOT_PYRE))
        except pyre.filesystem.GenericError:
            self.userfs = self.newFolder()
       # mount this directory as /pyre/user
        self["pyre/user"] = self.userfs

        return


    # constants
    DOT_PYRE = "~/.pyre"


# end of file 
