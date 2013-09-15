# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
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
            "class {.__name__!r} must implement 'start'".format(type(self)))


    def stop(self):
        raise NotImplementedError(
            "class {.__name__!r} must implement 'stop'".format(type(self)))


    def reset(self):
        raise NotImplementedError(
            "class {.__name__!r} must implement 'reset'".format(type(self)))


    def read(self):
        raise NotImplementedError(
            "class {.__name__!r} must implement 'read'".format(type(self)))


    def lap(self):
        raise NotImplementedError(
            "class {.__name__!r} must implement 'lap'".format(type(self)))


# end of file 
