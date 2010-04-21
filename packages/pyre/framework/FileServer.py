# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os
import re
from ..filesystem.Filesystem import Filesystem


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


    # interface
    def open(self, address, scheme=None, **kwds):
        """
        """
        # if {scheme} is missing, assume it is a file from the local filesystem
        if scheme is None or scheme == "file":
            return open(address, **kwds)

        # if {scheme} is 'vts', assume {address} is from our virtual filesystem
        if scheme == "vfs":
            return self[address].open()

        raise self.Bad


    # lower level interface
    def parseURI(self, uri):
        """
        Extract the scheme, address and fragment from {uri}.
        """
        # run uri through the recognizer
        match = self._uriRecognizer.match(uri)
        # if it fails to match, it must be malformed (or my regex is bad...)
        if match is None:
            raise self.BadResourceLocator(uri=uri, reason="unrecognizable")
        # extract the scheme
        scheme = match.group("scheme") or self.defaultMethod
        scheme = scheme.strip().lower()
        # extract the addres
        address = match.group("address")
        # check that it's not blank
        if not address:
            raise self.BadResourceLocator(uri=uri, reason="missing address")
        # extract the fragment
        fragment = match.group("fragment")
        # and return the triplet
        return scheme, address, fragment


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


    # exceptions
    from . import BadResourceLocator


    # constants
    DOT_PYRE = "~/.pyre"
    defaultMethod = "file"


    # private data
    _uriRecognizer = re.compile(
        r"((?P<scheme>[^:]+)://)?(?P<address>[^#]*)(#(?P<fragment>.*))?"
        )

    # from http://regexlib.com/Search.aspx?k=URL
    r"""
    ^(?=[^&])
    (?:(?<scheme>[^:/?#]+):)?
    (?://(?<authority>[^/?#]*))?
    (?<path>[^?#]*)(?:\?(?<query>[^#]*))?
    (?:#(?<fragment>.*))?
    """


# end of file 
