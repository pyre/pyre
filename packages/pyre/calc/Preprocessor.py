# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Preprocessor:
    """
    A mix-in class that performs arbitrary transformations on the value of a node
    """


    # types
    from ..schemata import identity
    from .exceptions import EvaluationError

    # public data
    preprocessor = None


    # interface
    def setValue(self, value, **kwds):
        """
        Intercept the node value setter and make sure that the value the caller gets has
        been through my {preprocessor}
        """
        # attempt to
        try:
            # process it
            value = self.preprocessor(value=value, node=self, **kwds)
        # protect against framework bugs: asking for configurable attributes that don't exist
        except AttributeError as error:
            # get the journal
            import journal
            # complain
            raise journal.firewall('pyre.calc').log(str(error))

        # and return it
        return super().setValue(value=value, **kwds)


    # meta-methods
    def __init__(self, preprocessor=identity.coerce, **kwds):
        # chain up
        super().__init__(**kwds)
        # set my value processor
        self.preprocessor = preprocessor
        # all done
        return


# end of file 
