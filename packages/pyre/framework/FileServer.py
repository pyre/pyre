# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os
import weakref
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
    their physical locations at runtime. For example, during the bootstrapping process the
    framework looks for user preferences for pyre applications. On Unix like machines, these
    are stored in '~/.pyre' and its subfolders. The entire hierarchy is mounted in the virtual
    filesystem under '/pyre/user'. This has the following advantages:

    * applications can navigate through the contents of '/user' as if it were an actual
      filesystem

    * configuration settings that require references to entries in '/pyre/user' can now be
      expressed portably, since there is no need to hardwire actual paths

    Applications are encouraged to lay out their own custom namespaces. The application
    developer can refer to resources through their standardized logical names, whereas the user
    is free to provide the mapping that reflects their physical location at runtime.
    """


    # constants
    DOT_PYRE = '~/.pyre'
    USER_DIR = '/pyre/user'
    STARTUP_DIR = '/pyre/startup'
    PACKAGES_DIR = '/pyre/packages'


    # public data
    @property
    def systemFolders(self):
        """
        Return the sequence of uris of the {pyre} system folders
        """
        # first the startup folder
        yield self.STARTUP_DIR
        # next the user folder
        yield self.USER_DIR
        # finally the packages folder
        yield self.PACKAGES_DIR
        # all done
        return


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
            return node.open(**kwds)

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
    def local(self, root, **kwds):
        """
        Build a local filesystem
        """
        # access the factory
        from .. import filesystem
        # invoke it
        return filesystem.local(root=root, **kwds)


    def virtual(self, **kwds):
        """
        Build a virtual filesystem
        """
        # access the factory
        from .. import filesystem
        # invoke it
        return filesystem.virtual(**kwds)


    # framework support
    def registerPackage(self, package):
        """
        Make the package configuration folder accessible in the virtual filesystem`
        """
        # This should be done very carefully because multiple packages may share a common
        # installation folder. For example, this is true of the packages that ship with the
        # standard pyre distribution. The registration procedure takes care not to mount
        # redundant filesystems in the virtual namespace.

        # grab the package prefix
        prefix = package.prefix
        # not much to do if there isn't one
        if not prefix: return package

        # otherwise, mount/get the associated filesystem
        fs = self.retrieveFilesystem(root=prefix)
        # attempt to
        try:
            # look for the configuration folder
            defaults = fs[package.DEFAULTS]
        # if not there
        except fs.NotFoundError:
            # nothing else to do
            return package

        # look for configuration files
        for encoding in self.executive.configurator.encodings():
            # build the configuration file name
            filename = "{}.{}".format(package.name, encoding)
            # look for
            try:
                # the node that corresponds to the configuration file
                cfgfile = defaults[filename]
            # if it's not there
            except fs.NotFoundError:
                # bail
                continue
            # if it is there, mount it at '/pyre/packages'
            self['{}/{}'.format(self.PACKAGES_DIR, filename)] = cfgfile

        # look for the configuration folder
        try:
            # get the associated node
            cfgdir = defaults[package.name]
        # if it's not there
        except fs.NotFoundError:
            # no problem
            pass
        # if it is there
        else:
            # attach it 
            self['{}/{}'.format(self.PACKAGES_DIR, package.name)] = cfgdir

        # all done
        return package


    def retrieveFilesystem(self, root):
        """
        Retrieve {root} if it is an already mounted filesystem; if not, mount it and return it
        """
        # check whether
        try:
            # i have seen this path before
            fs = self.mounts[root]
        # if not
        except KeyError:
            # no problem; make it
            fs = self.local(root=root).discover()
            # and remember it
            self.mounts[root] = fs

        # either way, return it
        return fs


    # meta-methods
    def __init__(self, executive=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # print("pyre.FileServer:")

        # remember my executive
        self.executive = None if executive is None else weakref.proxy(executive)

        # initialize the table of known mount points
        self.mounts = {}

        # build a place holder for package configuration hierarchies and mount it
        self[self.PACKAGES_DIR] = self.folder()

        # now, mount the user's home directory
        # the default location of user preferences is in ~/.pyre
        userdir = os.path.expanduser(self.DOT_PYRE) 
        # if that exists
        try:
            # make filesystem out of the preference directory
            user = self.local(root=userdir).discover()
        # otherwise
        except self.GenericError:
            # make an empty folder
            user = self.folder()
        # mount this directory as {/pyre/user}
        self[self.USER_DIR] = user

        # finally, mount the current working directory
        try:
            # make a filesystem out of the configuration directory
            startup = self.local(root=".").discover(levels=1)
        # if that fails
        except self.GenericError:
            # make an empty folder
            startup = self.folder()
       # mount this directory as {/pyre/startup}
        self[self.STARTUP_DIR] = startup

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
