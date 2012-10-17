# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os
from .. import schema
# superclass
from ..filesystem.Filesystem import Filesystem


# class declaration
class FileServer(Filesystem):
    """
    The manager of the virtual filesystem

    Instances of {FileServer} manage hierarchical namespaces implemented as a virtual
    filesystem. The contents of these namespaces are retrieved using URIs, and can be arbitrary
    objects, although they are typically either local or remote files.

    The framework uses a {FileServer} instance to decouple the logical names of resources from
    their physical locations at runtime. For example, as part of the bootstrapping process, the
    framework discovers the pyre installation directory; the persistent store for the default
    component configurations is a subdirectory of that location and it is mounted as
    '/pyre/system' in the virtual filesystem. This has the following benefits:
    
    * applications can navigate through the contents of '/pyre/system' as if it were an actual
      filesystem

    * configuration settings that require references to entries in '/pyre/system' can now be
      expressed portably, since there is no need to hardwire actual paths

    Similarly, user preferences are retrieved from '/pyre/user', which typically refers to the
    subdirectory '.pyre' of the user's home directory, but may be populated from other sources,
    depending on the operating system and the runtime environment.

    Applications are encouraged to lay out their own custom namespaces. The application
    developer can refer to resources through their standardized logical names, whereas the user
    is free to provide the mapping that reflects their physical location at runtime.
    """


    # constants
    DOT_PYRE = '~/.pyre'
    # public data
    prefixfs = None
    userfs = None
    startupfs = None


    # interface
    def open(self, uri, **kwds):
        """
        Convert {uri} into an input stream
        """
        # make sure {uri} is a {schema.uri}
        uri = schema.uri.coerce(uri)
        # get the {uri} scheme
        scheme = uri.scheme

        # if {scheme} is missing, assume it is a file from the local filesystem
        if scheme is None or scheme == 'file':
            # so attempt to
            try:
                # open it and return the associated file object
                return open(uri.address, **kwds)
            # if {uri} is not in my logical namespace
            except self.NotFoundError as error:
                # complain
                raise self.SourceNotFoundError(filesystem=self, node=error.node, uri=uri)
            # if {uri} maps to a non-existent file
            except IOError:
                # complain
                raise self.SourceNotFoundError(filesystem=self, node=None, uri=uri)

        # if the scheme is {vfs}
        if scheme == 'vfs':
            # assuming the uri is within my virtual filesystem
            try:
                # open it
                return self[uri.address].open()
            # if {uri} is not in my logical namespace
            except self.NotFoundError as error:
                # complain
                raise self.SourceNotFoundError(filesystem=self, node=error.node, uri=uri)

        # otherwise, complain
        raise self.URISpecificationError(uri=uri, reason="unsupported scheme {!r}".format(scheme))


    def splice(self, path, address, extension=None):
        """
        Join {path}, {address} and {extension} to form a valid pathname
        """
        # adjust the extension
        extension = '.' + extension if extension else ""
        # piece the parts together
        return "{}{}{}{}".format(path, self.separator, address, extension) 


    # convenience: access to the filesystem factories
    def local(self, **kwds):
        """
        Build a local filesystem
        """
        # access the factory
        from .. import filesystem
        # and invoke it
        return filesystem.local(**kwds)


    def virtual(self, **kwds):
        """
        Build a virtual filesystem
        """
        # access the factory
        from .. import filesystem
        # invoke it
        return filesystem.virtual(**kwds)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # print("pyre.FileServer:")

        # get access to the location where the framework is installed
        from .. import prefix as pyre_prefix

        # first, mount the system directory
        # there are two possibilities
        #  - it is an actual location on the disk
        #  - it is inside a zip file
        # the way to tell is by checking whether pyre.prefix() points to an actual directory
        # both are handled correctly by the {pyre.filesystem.local} factory
        try:
            # so invoke it to build the filesystem for us
            self.prefixfs = self.local(root=pyre_prefix()).discover(levels=1)
        # if this failed
        except self.GenericError:
            # just create a new empty folder
            system = self.folder()
        # otherwise
        else:
            # attempt to
            try:
                # hunt down the depository subdirectory
                system = self.prefixfs["defaults"]
            # if this failed
            except self.NotFoundError:
                # hmm... why is this directory missing from the distribution?
                # print(" ** warning: could not find system depository")
                # moving on...
                system = self.folder()
            # if successful
            else:
                # populate it with the disk contents
                system.discover(levels=1)
        # mount it as {/pyre/system}
        self["pyre/system"] = system

        # now, mount the user's home directory
        # the default location of user preferences is in ~/.pyre
        userdir = os.path.expanduser(self.DOT_PYRE) 
        try:
            # make filesystem out of the preference directory
            self.userfs = self.local(root=userdir).discover(levels=1)
        except self.GenericError:
            self.userfs = self.folder()
       # mount this directory as {/pyre/user}
        self["pyre/user"] = self.userfs

        # finally, mount the current working directory
        try:
            # make filesystem out of the preference directory
            self.startupfs = self.local(root=".").discover(levels=1)
        except self.GenericError:
            self.startupfs = self.folder()
       # mount this directory as {/pyre/startup}
        self["pyre/startup"] = self.startupfs

        # print("  prefix: {!r}".format(self.prefixfs.uri))
        # print("  system: {!r}".format(system.uri))
        # print("  user: {!r}".format(self.userfs.uri))
        # print("  startup: {!r}".format(self.startupfs.uri))
        # self.dump()

        # all done
        return


# end of file 
