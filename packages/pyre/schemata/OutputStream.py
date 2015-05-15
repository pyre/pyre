# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import sys
# superclasses
from .Schema import Schema
from ..framework.Dashboard import Dashboard


# declaration
class OutputStream(Schema, Dashboard):
    """
    A representation of input streams
    """


    # constants
    mode = 'w'
    typename = 'ostream'

    # types
    from . import uri


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into an open input stream
        """
        # the value is the special string "stdout"
        if value == 'stdout':
            # return the process stdout
            return sys.stdout
        # the value is the special string "stderr"
        if value == 'stderr':
            # return the process stderr
            return sys.stderr
        # if the {value} is a string or a uri
        if isinstance(value, str) or isinstance(value, self.uri.locator):
            # assume that the framework fileserver knows how to deal with it
            return self.pyre_fileserver.open(uri=value, mode=self.mode)
        # otherwise, leave it alone
        return value


    # meta-methods
    def __init__(self, default='stdout', mode=mode, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # save my mode
        self.mode = mode
        # all done
        return


# end of file
