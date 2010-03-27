# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre.framework


class Executive(object):

    """
    The top level framework object.

    Executive maintains the following suite of objects that provide the various mechanisms and
    policies that enable pyre applications:

        NYI:
    """


    def boot(self):
        """
        Perform all the default initialization steps
        """


    def __init__(self, **kwds):
        super().__init__(**kwds)


        # my codec manager
        self.codecs = pyre.framework.newCodecManager()
        # my virtual filesystem
        self.fileserver = pyre.framework.newFileServer()

        return


# end of file 
