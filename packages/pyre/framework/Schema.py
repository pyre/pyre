# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# class declaration
class Schema:
    """
    The singleton that indexes the database schema of a pyre application
    """


    # public data
    models = None # a map of tables to objects that model them


    # meta-methods
    def __init__(self, executive, **kwds):
        # chain up
        super().__init__(**kwds)
        # set up my model index
        self.models = {}
        # all done
        return


# end of file 
