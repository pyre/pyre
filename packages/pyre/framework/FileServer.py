# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os
from .. import schemata
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
    '/system/pyre' in the virtual filesystem. This has the following benefits:
    
    * applications can navigate through the contents of '/system/pyre' as if it were an actual
      filesystem

    * configuration settings that require references to entries in '/system/pyre' can now be
      expressed portably, since there is no need to hardwire actual paths

    Similarly, user preferences are retrieved from '/user', which typically refers to the
    subdirectory '.pyre' of the user's home directory, but may be populated from other sources,
    depending on the operating system and the runtime environment.

    Applications are encouraged to lay out their own custom namespaces. The application
    developer can refer to resources through their standardized logical names, whereas the user
    is free to provide the mapping that reflects their physical location at runtime.
    """


    # constants
    DOT_PYRE = '~/.pyre'


    # interface
    def open(self, uri, **kwds):
        """
        Convert {uri} into an input stream
        """
        # make sure {uri} is a {schemata.uri} instance
        uri = schemata.uri().coerce(uri)
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
            # if {uri} maps to a folder
            except OSError: # NYI: after python3.3: convert to IsADirectoryError
                # complain
                raise self.IsFolderError(filesystem=self, node=None, uri=uri)

        # if the scheme is {vfs}
        if scheme == 'vfs':
            # assuming the uri is within my virtual filesystem
            try:
                # get the node
                node = self[uri.address]
            # if {uri} is not in my logical namespace
            except self.NotFoundError as error:
                # complain
                raise self.SourceNotFoundError(filesystem=self, node=error.node, uri=uri)

            # if the node is a folder
            if node.isFolder:
                # complain
                raise self.IsFolderError(filesystem=self, node=node, uri=uri)
            # otherwise, open it
            return node.open()

        # if i didn't recognize the {scheme}, complain
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
        from .. import defaults as pyre_defaults

        # first, mount the system directory
        # there are two possibilities
        #  - it is an actual location on the disk
        #  - it is inside a zip file
        # the way to tell is by checking whether {pyre.prefix} points to an actual directory
        # both are handled correctly by the {pyre.filesystem.local} factory
        try:
            # so invoke it to build the filesystem for us
            system = self.local(root=pyre_defaults).discover()
        # if this failed
        except self.GenericError:
            # just create a new empty folder
            system = self.folder()
        # mount it as {/system/pyre}
        self["system"] = system

        # now, mount the user's home directory
        # the default location of user preferences is in ~/.pyre
        userdir = os.path.expanduser(self.DOT_PYRE) 
        try:
            # make filesystem out of the preference directory
            user = self.local(root=userdir).discover()
        except self.GenericError:
            user = self.folder()
       # mount this directory as {/user}
        self["user"] = user

        # finally, mount the current working directory
        try:
            # make a filesystem out of the configuration directory
            startup = self.local(root=".").discover(levels=1)
        except self.GenericError:
            startup = self.folder()
       # mount this directory as {/startup}
        self["startup"] = startup

        # all done
        return


    # debugging
    def draw(self, *paths):
        """
        Draw the contents of the nodes in {paths}
        """
        # assess the workload
        paths = paths if paths else [ '/']
        # go through the pile
        for path in paths:
            # get the associated node
            node = self[path]
            # leave a marker
            print(" ** {}:".format(path))
            # draw the contents
            node.dump(indent=' '*4)
        # all done
        return


# end of file 
