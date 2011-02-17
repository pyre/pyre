# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import os
from ..filesystem.Filesystem import Filesystem


class FileServer(Filesystem):

    """
    The manager of the virtual filesystem

    Instances of FileServer manage hierarchical namespaces implemented as a virtual
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


    # interface
    def open(self, scheme, address, **kwds):
        """
        """
        # get the extension 
        path, extension = os.path.splitext(address)
        # deduce the encoding based on the file extension
        encoding = extension[1:]

        # if {scheme} is missing, assume it is a file from the local filesystem
        if scheme is None or scheme == "file":
            try:
                return encoding, open(address, **kwds)
            except IOError as error:
                raise self.NotFoundError(filesystem=self, node=None, path=address, fragment='file')

        # if {scheme} is 'vfs', assume {address} is from our virtual filesystem
        if scheme == "vfs":
            return encoding, self[address].open()

        # oops: the file server doesn't know what to do with this
        # piece back the uri
        uri = "{}://{}".format(scheme, address)
        # and raise an exception
        raise self.URISpecificationError(
            uri=uri, reason="unsupported scheme {!r}".format(scheme))


    def join(self, path, address, extension=None):
        """
        Join {path}, {address} and {extension} to form a valid pathname
        """
        # adjust the extension
        extension = '.' + extension if extension else ""
        # piece the parts together
        return "{}{}{}{}".format(path, self.PATH_SEPARATOR, address, extension) 


    # lower level interface
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
            self.systemfs = pyre.filesystem.newFilesystem(pyre.prefix()).sync(levels=1)
        except self.GenericError:
            # if this failed, just create a new empty folder
            system = self.newFolder()
        else:
            try:
                # hunt down the depository subdirectory
                system = self.systemfs["depository"]
            except self.NotFoundError:
                # hmm... why is this directory missing from the distribution?
                # moving on...
                system = self.newFolder()
       # mount the system directory
        self["pyre/system"] = system

        # now, mount the user's home directory
        # the default location of user preferences is in ~/.pyre
        userdir = os.path.expanduser(self.DOT_PYRE) 
        try:
            # make filesystem out of the preference directory
            self.userfs = pyre.filesystem.newFilesystem(userdir).sync(levels=1)
        except self.GenericError:
            self.userfs = self.newFolder()
       # mount this directory as /pyre/user
        self["pyre/user"] = self.userfs

        # finally, mount the current working directory
        try:
            # make filesystem out of the preference directory
            self.localfs = pyre.filesystem.newFilesystem(".").sync(levels=1)
        except self.GenericError:
            self.localfs = self.newFolder()
       # mount this directory as /local
        self["local"] = self.localfs

        return


    # exceptions
    from ..filesystem.exceptions import NotFoundError, URISpecificationError


    # constants
    DOT_PYRE = "~/.pyre"


# end of file 
