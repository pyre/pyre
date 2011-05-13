# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import collections


# super-classes
from .Channel import Channel
from .Diagnostic import Diagnostic


# declaration
class Warning(Diagnostic, Channel):
    """
    This class is the implementation of the warning channel
    """


    # public data
    severity = "warning"


    # meta methods
    def __init__(self, name, **kwds):
        # chain to my ancestors
        super().__init__(name=name, inventory=self._index[name], **kwds)
        # and return
        return


    # implementation details
    # types
    class _State:
        # public data
        state = True
        device = None


    # class private data
    _index = collections.defaultdict(_State)


# end of file 
