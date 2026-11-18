#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the metaclass correctly builds document and element handlers out of the
    associated declarations
    """
    # access the package
    import pyre.xml

    # the base class of the element handlers
    from pyre.xml.Node import Node

    # and of documents
    from pyre.xml.Document import Document

    # the document structure
    class Owner(Node):
        """
        Handle the owner tag
        """

    class Permissions(Node):
        """
        Handle the permissions tag
        """

    class File(Node):
        """
        Handle the file tag
        """

        # the tags it may contain
        elements = ("owner", "permissions")

    class Folder(Node):
        """
        Handle the folder tag
        """

        # the tags it may contain
        elements = ("owner", "permissions", "file", "folder")

    class Filesystem(Folder):
        """
        The top level document element
        """

    class FSD(Document):
        """
        Document class
        """

        # the element descriptors: the root
        filesystem = pyre.xml.element(tag="filesystem", handler=Filesystem, root=True)
        # the owner
        owner = pyre.xml.element(tag="owner", handler=Owner)
        # the permissions
        permissions = pyre.xml.element(tag="permissions", handler=Permissions)
        # a file
        file = pyre.xml.element(tag="file", handler=File)
        # and a folder
        folder = pyre.xml.element(tag="folder", handler=Folder)

    # verify that the descriptors were correctly harvested by the metaclass
    assert FSD.dtd == (FSD.filesystem, FSD.owner, FSD.permissions, FSD.file, FSD.folder)

    # verify that each node has the right (tag, handler constructor) map: owners hold nothing
    assert Owner._pyre_nodeIndex == {}
    # neither do permissions
    assert Permissions._pyre_nodeIndex == {}
    # files hold owners and permissions
    assert File._pyre_nodeIndex == {"owner": Owner, "permissions": Permissions}
    # folders hold those, plus files and other folders
    assert Folder._pyre_nodeIndex == {
        "owner": Owner,
        "permissions": Permissions,
        "file": File,
        "folder": Folder,
    }
    # and the filesystem inherits its map from the folder
    assert Filesystem._pyre_nodeIndex == {
        "owner": Owner,
        "permissions": Permissions,
        "file": File,
        "folder": Folder,
    }

    # all done
    return FSD


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
