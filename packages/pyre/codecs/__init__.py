# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This package contains the implementation of the readers and writers of the various
configuration file formats supported by pyre.

"""


# factory
def newManager(**kwds):
    from .CodecManager import CodecManager
    return CodecManager(**kwds)


# end of file
