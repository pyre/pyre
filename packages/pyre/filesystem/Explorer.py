# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Explorer:
    """
    Base class for visitors of the filesystem object model
    """


    def onNode(self, node, **kwds):
        """
        Handler for generic nodes
        """
        return


    def onFolder(self, folder, **kwds):
        """
        Handler for generic folders
        """
        return


# end of file 
