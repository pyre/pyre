# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import pyre


# class declaration
class Repertoir:
    """
    The manager of the collection of installed actions
    """


    # meta-methods
    def __init__(self, protocol, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the protocol
        self.protocol = protocol
        # all done
        return


    # implementation details
    # data
    protocol = None
        

# end of file 
