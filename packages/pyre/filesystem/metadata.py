# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

"""
This module contains the base classes for the filesystem node meta-data
"""

# class declarations
class Info:
    """
    Base class for encapsulating nodal metadata for filesystem entries
    """

    # meta methods
    def __init__(self, uri, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the node uri
        self.uri = uri
        # all done
        return

    # implementation details
    __slots__ = ('uri',)


class NodeInfo(Info):
    """
    Metadata for leaf nodes
    """

    # constant
    marker = 'f'

    # implementation details
    __slots__ = ()


class FolderInfo(Info):
    """
    Metadata for container nodes
    """

    # constant
    marker = 'd'

    # implementation details
    __slots__ = ()


class ZipNode(NodeInfo):
    """
    Metadata for zip file contents that are leaves
    """

    # meta methods
    def __init__(self, zipinfo, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the information stored by the zip archive
        self.zipinfo = zipinfo
        # all done
        return

    # implementation details
    __slots__ = ('zipinfo', )


class ZipFolder(FolderInfo):
    """
    Metadata for zip file contents that are containers
    """

    # meta methods
    def __init__(self, zipinfo, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the information stored by the zip archive
        self.zipinfo = zipinfo
        # all done
        return

    # implementation details
    __slots__ = ('zipinfo', )


# end of file
