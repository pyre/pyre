# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# ancestor
from ..patterns.Named import Named


# declaration
class AbstractTimer(Named):
    """
    Base class for timers
    """


    # interface
    def start(self):
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'start'".format(self))


    def stop(self):
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'stop'".format(self))


    def reset(self):
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'reset'".format(self))


    def read(self):
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'read'".format(self))


    def lap(self):
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'lap'".format(self))


# end of file 
