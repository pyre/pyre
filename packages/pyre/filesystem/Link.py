# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# superclass
from .Info import Info
from .InfoStat import InfoStat


# class declaration
class Link(InfoStat, Info):
    """
    Representation of symbolic links for filesystems that support them
    """


    # public data
    @property
    def marker(self):
        """
        Get the marker of the referent
        """
        # ask...
        return self.referent.marker


    @property
    def isFolder(self):
        """
        Check whether this is a link to a directory
        """
        # ask...
        return self.referent.isFolder


    # interface
    def identify(self, explorer, **kwds):
        """
        Guide {explorer}
        """
        return explorer.onLink(info=self, **kwds)


    # meta-methods
    def __init__(self, uri, info=None, **kwds):
        # chain up
        super().__init__(uri=uri, info=info, **kwds)

        # support
        from .Stat import Stat
        # build my referent
        self.referent = Stat.recognize(entry=uri, follow_symlinks=True)

        # all done
        return


    def __bool__(self):
        # check for broken links
        return self.referent is not None


# end of file
