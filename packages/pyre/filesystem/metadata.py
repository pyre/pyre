# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# class declarations
class Info:
    """
    Base class for encapsulating nodal metadata for filesystem entries
    """

    # meta methods
    def __init__(self, uri, **kwds):
        super().__init__(**kwds)
        self.uri = uri
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
        super().__init__(**kwds)
        self.zipinfo = zipinfo
        return

    # implementation details
    __slots__ = ('zipinfo', )


class ZipFolder(FolderInfo):
    """
    Metadata for zip file contents that are containers
    """

    # meta methods
    def __init__(self, zipinfo, **kwds):
        super().__init__(**kwds)
        self.zipinfo = zipinfo
        return

    # implementation details
    __slots__ = ('zipinfo', )


# end of file 
