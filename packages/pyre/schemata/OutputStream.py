# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import sys
# superclasses
from .Type import Type
from ..framework.Client import Client


# declaration
class OutputStream(Type, Client):
    """
    A representation of input streams
    """


    # constants
    mode = 'w'
    default = 'stdout'
    typename = 'ostream'
    

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into an open input stream
        """
        # the value is the special string {stdout}
        if value == 'stdout':
            # return the process stdout
            return sys.stdout
        # the value is the special string {stderr}
        if value == 'stderr':
            # return the process stderr
            return sys.stderr
        # if the {value} is a string
        if isinstance(value, str):
            # assume it is a uri that the framework fileserver knows how to deal with
            return self.pyre_fileserver.open(uri=value, mode=self.mode)
        # otherwise, leave it alone
        return value
        

    # meta-methods
    def __init__(self, default=default, mode=mode, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # save my mode
        self.mode = mode
        # all done
        return


# end of file 
