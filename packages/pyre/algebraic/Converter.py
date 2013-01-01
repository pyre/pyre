# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Converter:
    """
    A mix-in class that ensures node values have undergone special processing
    """


    # types
    from ..schema import identity
    from .exceptions import EvaluationError

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
        # attempt to
        try:
            # process it
            value = self.converter(value=value, node=self, **kwds)
        # protect against framework bugs: asking for configurable attributes that don't exist
        except AttributeError as error:
            # complain carefully to avoid infinite recursions
            # NYI: can i do journal here?
            raise self.EvaluationError(node=self, error=str(error))

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
