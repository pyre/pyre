# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Converter:
    """
    A mix-in class that ensures node values have undergone special processing
    """


    # types
    from ..schema import identity

    # public data
    converter = None


    # interface
    def getValue(self, **kwds):
        """
        Intercept the node value retriever and make sure that the value the caller gets has
        been through my {converter}
        """
        # get the value
        value = super().getValue()
        # process it
        value = self.converter(value=value, node=self, **kwds)
        # and return it
        return value


    # meta-methods
    def __init__(self, converter=identity.coerce, **kwds):
        # chain up
        super().__init__(**kwds)
        # set my value processor
        self.converter = converter
        # all done
        return


# end of file 
