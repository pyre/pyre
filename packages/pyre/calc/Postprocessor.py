# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Postprocessor:
    """
    A mix-in class that performs arbitrary transformations on the value of a node
    """


    # types
    from ..schemata import identity
    from .exceptions import EvaluationError

    # public data
    postprocessor = None


    # interface
    def getValue(self, **kwds):
        """
        Intercept the node value retriever and make sure that the value the caller gets has
        been through my {postprocessor}
        """
        # get the value
        value = super().getValue()
        # attempt to
        try:
            # process it
            value = self.postprocessor(value=value, node=self, **kwds)
        # protect against framework bugs: asking for configurable attributes that don't exist
        except AttributeError as error:
            # get the journal
            import journal
            # complain
            raise journal.firewall('pyre.calc').log(str(error))

        # and return it
        return value


    # meta-methods
    def __init__(self, postprocessor=identity.coerce, **kwds):
        # chain up
        super().__init__(**kwds)
        # set my value processor
        self.postprocessor = postprocessor
        # all done
        return


# end of file 
